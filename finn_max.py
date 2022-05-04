import json

with open("files.json") as f:
    fil = json.load(f)

einskild_max = 0
einskild_namn = "i"
total_max = 0 
total_namn = "j"
total_tal = 0
for f in fil:

    if 'Size' in fil[f][0] and fil[f][0]['Size'] > einskild_max:
        einskild_max = fil[f][0]['Size']
        einskild_namn = fil[f][0]['Path']
        print("størst ",einskild_namn,einskild_max/(1024**3))
    samla_sum = 0
    for a in fil[f]:
        if 'Size' in fil[f][0]:
            samla_sum += a['Size']
    if samla_sum > total_max:
        total_namn =  fil[f][0]['Path']
        total_max = samla_sum
        total_tal = len(fil[f])
        print("max ",total_namn,total_max/(1024**3), total_tal)

print("største fil er ", einskild_namn, " som er ", einskild_max/(1024**3)," GB stor")
print("fila med størst avtrykk er ", total_namn, "som er ", total_tal, " og brukar ", total_max/(1024**3) , "GB")