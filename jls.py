import subprocess
import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("root_folder")
parser.add_argument("filepath")

args = parser.parse_args()

def hentls(path):
  children =  json.loads(subprocess.run(["jotta-cli.exe", "ls", "--json", path], 
        capture_output=True, text=True).stdout)
  if 'Folders' in children:
    for child in children['Folders']:
      child['Children'] = hentls(child['Path'])
  return children



root_folder = args.root_folder

root = json.loads(subprocess.run(["jotta-cli.exe", "ls", "--json", root_folder], 
      capture_output=True, text=True).stdout)

for folder in root['Folders']:
  folder['Children'] = hentls(folder['Path'])

with open(args.filepath, 'w', encoding='utf-8') as f:
  json.dump(root, f, indent=4, ensure_ascii=False, sort_keys=True)
