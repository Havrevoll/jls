import subprocess
import json
import argparse
import datetime

parser = argparse.ArgumentParser()
parser.add_argument("root_folder")
parser.add_argument("filepath")

args = parser.parse_args()

def hentls(path):
  try:
    children =  json.loads(subprocess.run(["jotta-cli.exe", "ls", "--json", path], 
        capture_output=True, text=True).stdout)
  except ValueError:
    return "Empty"
  if 'Folders' in children:
    for child in children['Folders']:
      child['Children'] = hentls(child['Path'], level = level +1)
  return children



root_folder = args.root_folder

root = json.loads(subprocess.run(["jotta-cli.exe", "ls", "--json", root_folder], 
      capture_output=True, text=True).stdout)

for folder in root['Folders']:
  folder['Children'] = hentls(folder['Path'])

with open(args.filepath, 'w', encoding='utf-8') as f:
  json.dump(root, f, indent=4, ensure_ascii=False, sort_keys=True)


your_dt = datetime.datetime.fromtimestamp(int(timestamp)/1000)                                                                                                                                                     

print(your_dt.strftime("%Y-%m-%d %H:%M:%S"))