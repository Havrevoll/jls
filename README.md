# jls
Eit program for å få oversyn over filene i Jottacloud, med hjelp av jotta-cli og python.

Lagar to databasar/dicts:
- Alle filer med md5sum som key og value ei liste med ein dict for kvar stad med fylgjande informasjon:
  - Namn (som er full sti)
  - Filnamn
  - Storleik
  - Endra
  - Laga
- Alle mapper som er ein dict med namn (som er full sti) som key og som value ein dict med fylgjande informasjon:
  - filer som er ein dict med fylgjande informasjon:
    - Namn ( som er full sti)
    - Filnamn
    - Storleik
    - MD5sum
    - Endra dato
    - Laga dato
  - mapper som er ei liste med fylgjande informasjon:
    - Undermapper

I grunnen er dette berre ein kopi av JSON-fila som kjem frå kvart søk på ei mappe. Ganske enkelt.

Deretter må det vera eit slags menysystem for å henta informasjon:
- Finn alle mapper som har heilt like innhald.
- Finn ut om innhaldet i ei mappe finst andre stader, og list opp andre mapper som har komplett eller delvis komplett kopi, rangert.
- 