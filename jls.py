import subprocess
import json
import argparse
from collections import defaultdict
from pathlib import Path
import datetime

#from requests import JSONDecodeError

#%%

parser = argparse.ArgumentParser()
parser.add_argument("root_folder", nargs='?')
parser.add_argument("folder_savepath", nargs='?')
parser.add_argument("files_savepath", nargs='?')
args = parser.parse_args()

if args.root_folder is None:
  root_folder = ""
else:
  root_folder = args.root_folder
if args.folder_savepath is None:
  folder_savepath = 'folders.json'
else:
  folder_savepath = args.folder_savepath
if args.files_savepath is None:
  files_savepath = 'files.json'
else:
  files_savepath = args.files_savepath

file_collection = defaultdict(list)

def hentls(path, level=0):
  if level < 7:
    print("Er på nivå ", level, ", ", path)
  try:
    children =  json.loads(subprocess.run(["jotta-cli", "ls", "--json", path], 
        capture_output=True, text=True).stdout)
  except ValueError:
    return "Empty"
  if 'Folders' in children:
    for child in children['Folders']:
      size = 0
      try:
        # if child['Name'] != 'Trash':
          content = hentls(child['Path'], level = level +1)
        # else:
        #   content = {}
      except KeyError:
        if child['Name'] == 'Backup' and 'Path' not in child:
          print(f"Eg er i {path} og gjekk i keyerror")
          content = hentls("Backup", level= level+1)
      if 'Files' in content:
        child['Files'] = content['Files']
        for file in child['Files']:
          size += file['Size']

      if 'Folders' in content:
        child['Folders'] = content['Folders']
        for folder in child['Folders']:
          size += folder['Size']
      child['Size'] = size

  if 'Files' in children:
    for file in children['Files']:
      if 'Size' not in file:
        file['Size'] = 0
      file_collection[file['Checksum']].append(file)
  return children
import ray
ray.init()

@ray.remote
def hentls_remote(path, level=0):
  if level < 7:
    print("Er på nivå ", level, ", ", path)
  try:
    children =  json.loads(subprocess.run(["jotta-cli", "ls", "--json", path], 
        capture_output=True, text=True).stdout)
  except ValueError:
    return "Empty"
  if 'Folders' in children:
    for child in children['Folders']:
      size = 0
      try:
        # if child['Name'] != 'Trash':
          content = hentls(child['Path'], level = level +1)
        # else:
        #   content = {}
      except KeyError:
        if child['Name'] == 'Backup' and 'Path' not in child:
          print(f"Eg er i {path} og gjekk i keyerror")
          content = hentls("Backup", level= level+1)
      if 'Files' in content:
        child['Files'] = content['Files']
        for file in child['Files']:
          size += file['Size']

      if 'Folders' in content:
        child['Folders'] = content['Folders']
        for folder in child['Folders']:
          size += folder['Size']
      child['Size'] = size

  if 'Files' in children:
    for file in children['Files']:
      if 'Size' not in file:
        file['Size'] = 0
      file_collection[file['Checksum']].append(file)
  return children

start = datetime.datetime.now()

tree = json.loads(subprocess.run(["jotta-cli", "ls", "--json", root_folder], capture_output=True, text=True).stdout)

for a in tree['Folders']:
  if 'Path' not in a:
    a['Path'] = '/backup/'

archive_job = hentls_remote.remote('/archive/')
backup_job = hentls_remote.remote('/backup/')
sync_job = hentls_remote.remote('/sync/')
photo_job = hentls_remote.remote('/photos/')
jobbane = {archive_job:0,backup_job:1, photo_job:2, sync_job:3 }
unready = [archive_job,backup_job,sync_job,photo_job]
while True:
  ready, unready = ray.wait(unready)
  ferdig = ray.get(ready[0])
  size = 0
  if 'Files' in ferdig:
    for file in ferdig['Files']:
          size += file['Size']
    tree['Folders'][jobbane[ready[0]]]['Files'] = ferdig['Files']
  if 'Folders' in ferdig:
    for folder in ferdig['Folders']:
          size += folder['Size']
    tree['Folders'][jobbane[ready[0]]]['Folders'] = ferdig['Folders']
    tree['Folders'][jobbane[ready[0]]]['Size'] = size
  if len(unready) == 0:
    break

# tree = hentls(root_folder)
tree['Path'] = root_folder
if tree['Folders'][-1]['Name'] == 'Trash':
  tree['Folders'].pop()

root_folder = Path(root_folder)

tree['Name'] = root_folder.name
size = 0
if 'Files' in tree:
  for file in tree['Files']:
    size += file['Size']
if 'Folders' in tree:
        for folder in tree['Folders']:
          size += folder['Size']
tree['Size'] = size

# for folder in tree['Folders']:
#   print(folder['Name'])
#   if 'Path' in folder and folder['Name'] != 'Trash':

#     folder['Children'] = hentls(folder['Path'])
#   elif folder['Name'] == "Backup":
#     folder['Children'] = hentls('Backup')

with open(folder_savepath, 'w', encoding='utf-8') as f:
  json.dump(tree, f, indent=4, ensure_ascii=False, sort_keys=True)
with open(files_savepath, 'w', encoding='utf-8') as f:
  json.dump(file_collection, f, indent=4, ensure_ascii=False, sort_keys=True)

# your_dt = datetime.datetime.fromtimestamp(int(timestamp)/1000)                                                                                                                                                     

# print(your_dt.strftime("%Y-%m-%d %H:%M:%S"))
print(f"Ferdig, brukte {datetime.datetime.now()-start} på jobben")
