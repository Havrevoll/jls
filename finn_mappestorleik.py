import json

with open('folders.json') as f:
    tree = json.load(f)

def get_size(folder):
    folder_size = 0
    if 'Folders' in folder:
        for child in folder['Folders']:
            size = get_size(child['Children'])
            folder_size += size
    if 'Files' in folder:
        for child in folder['Files']:
            if 'Size' in child:
                size = child['Size']
            else: 
                size = 0
            folder_size += size
    return folder_size

total_size = get_size(tree)
print(total_size/(1024**3)," GB")
