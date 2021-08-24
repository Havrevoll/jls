import subprocess
import json

root_folder = sys.argv[1]

root = json.loads(subprocess.run(["jotta-cli.exe", "ls", "--json", "--l", root_folder[0]], capture_output=True, text=True).stdout)

for folder in root['Folders']:
  folder['Children'] = hentls(folder['Path'])

def hentls(path):
  children =  json.loads(subprocess.run(["jotta-cli.exe", "ls", "--json", "--l", path], capture_output=True, text=True).stdout)
  for child in children['Folders']:
    child['Children'] = hentls(child['Path'])
  return children

json.dump(root, './folders.json', indent=4, sort_keys=True)
