import json
import argparse
import pprint

def search(d, search_pattern, prev_datapoint_path=''):
    '''https://stackoverflow.com/questions/22162321/search-for-a-value-in-a-nested-dictionary-python'''
    output = []
    current_datapoint = d
    current_datapoint_path = prev_datapoint_path
    if type(current_datapoint) is dict:
        for dkey in current_datapoint:
            if search_pattern in str(dkey):
                c = current_datapoint_path
                c+="['"+dkey+"']"
                output.append(c)
            c = current_datapoint_path
            c+="['"+dkey+"']"
            for i in search(current_datapoint[dkey], search_pattern, c):
                output.append(i)
    elif type(current_datapoint) is list:
        for i in range(0, len(current_datapoint)):
            if search_pattern in str(i):
                c = current_datapoint_path
                c += "[" + str(i) + "]"
                output.append(i)
            c = current_datapoint_path
            c+="["+ str(i) +"]"
            for i in search(current_datapoint[i], search_pattern, c):
                output.append(i)
    elif search_pattern in str(current_datapoint):
        c = current_datapoint_path
        output.append(c)
    output = filter(None, output)
    return list(output)

parser = argparse.ArgumentParser()
parser.add_argument("check_folder", nargs='?')
parser.add_argument("files", nargs='?')
parser.add_argument("folders", nargs='?')
args = parser.parse_args()

if args.check_folder is None:
  check_folder = "/archive/Tidlegare tryggingskopiar/ola iphone/Camera uploads/"
else:
  check_folder = args.check_folder
if args.files is None:
  files = "files.json"
else:
  files = args.files
if args.folders is None:
  folders = "folders.json"
else:
  folders = args.folders

with open(folders) as folder_file:
    folder_tree = json.load(folder_file)

