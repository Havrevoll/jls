import subprocess
import json
import argparse
from collections import defaultdict

#from requests import JSONDecodeError

#%%

parser = argparse.ArgumentParser()
parser.add_argument("root_folder", nargs='?')
parser.add_argument("folder_savepath", nargs='?')
parser.add_argument("files_savepath", nargs='?')
args = parser.parse_args()

if args.root_folder is None:
  root_folder = "/archive/"
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
  print("Er på nivå ", level, ", ", path)
  try:
    children =  json.loads(subprocess.run(["jotta-cli", "ls", "--json", path], 
        capture_output=True, text=True).stdout)
  except ValueError:
    return "Empty"
  if 'Folders' in children:
    for child in children['Folders']:
      child['Children'] = hentls(child['Path'], level = level +1)

  if 'Files' in children:
    for file in children['Files']:
      file_collection[file['Checksum']].append(file)
  return children


tree = json.loads(subprocess.run(["jotta-cli", "ls", "--json", root_folder], capture_output=True, text=True).stdout)

for folder in tree['Folders']:
  folder['Children'] = hentls(folder['Path'])

with open(folder_savepath, 'w', encoding='utf-8') as f:
  json.dump(tree, f, indent=4, ensure_ascii=False, sort_keys=True)
with open(files_savepath, 'w', encoding='utf-8') as f:
  json.dump(file_collection, f, indent=4, ensure_ascii=False, sort_keys=True)

# your_dt = datetime.datetime.fromtimestamp(int(timestamp)/1000)                                                                                                                                                     

# print(your_dt.strftime("%Y-%m-%d %H:%M:%S"))
