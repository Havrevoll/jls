import json
import pickle
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("root_folder")
parser.add_argument("out_file")

args = parser.parse_args()

root_folder = args.root_folder
out_file = args.out_file

root = json.loads(subprocess.run(["jotta-cli", "ls", "--json", "--l", root_folder], capture_output=True, text=True).stdout)

chksms = {} 
for f in root['Files']: 
    chksms[f['Checksum']] = f['Path'] 

with open(out_file, 'wb') as f:
    pickle.dump(chksms, f)

