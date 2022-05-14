import json
from pathlib import Path

with open('f_fo.json') as f:
    fo = json.load(f)

with open('f_fi.json') as f:
    fi = json.load(f)
del f

from oper import show,samanlikna

samanlikna(fo,fi)