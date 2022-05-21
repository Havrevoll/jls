import json
from pathlib import Path

with open('folders.json') as f:
    fo = json.load(f)
    assert fo['Folders'][1]['Name'] == 'Backup'
    fo['Folders'][1]['Path'] = '/backup/'

with open('files.json') as f:
    fi = json.load(f)
del f



from oper import show,samanlikna, get_children

