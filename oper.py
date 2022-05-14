from pathlib import Path
import subprocess
import time
import inotify.adapters

def get_children2(path, fi):
    samla = []
    for a in fi:
         liste = [a for b in fi[a] if path in Path(b['Path']).parents]
         if len(liste)>0:
             samla.append(liste[0])
    return samla


def get_children(folder):
    children = []
    if 'Folders' in folder:
        for child in folder['Folders']:
            children.extend(get_children(child))
    if 'Files' in folder:
        for child in folder['Files']:
            children.append(child['Checksum'])
    return children

def show(co):
    if not 'Folders' in co:
        print(f"Ingen mapper under {co['Path']}, returnerer")
        return co
    print(f"No er me i {co['Path']}")
    [print(i,a['Path']) for i,a in enumerate(co['Folders'])]
    no = int(input("Kva mappenummer? "))
    if no <0:
        return co
    else:
        return show(co['Folders'][no])

def samanlikna(co,fi):
    print("Sjekk om alt i...")
    fyrste = show(co)
    print("Finst i denne...")
    andre = show(co)

    fyrste_filer = get_children(fyrste)
    andre_filer = get_children(andre)
    teljar = 0
    liste_over_filer_som_fanst_i_fyrste_mappe_men_ikkje_i_andre = []

    for fil in fyrste_filer:
        if fil not in andre_filer:
            teljar += 1
            fyrste_mappe_sti = Path(fyrste['Path'])
            for stad in fi[fil]:
                foreldra = Path(stad['Path']).parents
                if fyrste_mappe_sti in foreldra:
                    kva_heiter_fila_i_fyrste = Path(stad['Path'])
                    liste_over_filer_som_fanst_i_fyrste_mappe_men_ikkje_i_andre.append(kva_heiter_fila_i_fyrste)
                    break

            print(f"Ei fil frå fyrste mappe ({kva_heiter_fila_i_fyrste}) fanst ikkje i andre mappe ({andre['Path']}). Den finst her òg:")
            for stad in fi[fil]:
                print(stad['Path'])
            print(" ")
    if teljar > 0:
        print(f"Det var {teljar} filer av {len(fyrste_filer)} i fyrste mappa som ikkje var i andre mappa, der det var {len(andre_filer)} filer.")
        val = input("Vil du flytta dei over (det tek lang tid)? ").lower()
        if val == "ja" or val == "j":
            i = inotify.adapters.Inotify()
            i.add_watch(str(Path.cwd().joinpath('taa')))
            for fil in liste_over_filer_som_fanst_i_fyrste_mappe_men_ikkje_i_andre:
                fil_i_undermappe = Path('./taa').joinpath(fil.name)
                if not fil_i_undermappe.exists():
                    subprocess.run(["jotta-cli", "download", fil, "./taa"])
                    for event in i.event_gen(yield_nones=False):
                        (_, type_names,_, filename) = event
                        # print(fil.name, type_names, filename, 'IN_CLOSE_WRITE' in type_names) 
                        if 'IN_CLOSE_WRITE' in type_names and filename == str(fil.name):
                            print("kom her")
                            break
                    # print("PATH=[{}] FILENAME=[{}] EVENT_TYPES={}".format(path, filename, type_names))

                subprocess.run(["jotta-cli", "archive", fil_i_undermappe, f"--remote={Path(andre['Path']).joinpath(fil.name)}", "--nogui"])
                fil_i_undermappe.unlink()

    else: 
        print(f"Det var ingen av dei {len(fyrste_filer)} filene i fyrste mappa ({fyrste['Path']}) som ikkje var i andre mappa ({andre['Path']}), der det var {len(andre_filer)} filer.")