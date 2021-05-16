"""
Proiect LP2
Echipa: 11-E7
Studenti: Bakcsi Silviu-Daniel; Balog Csaba-Norbert
Tema Proiect: D3-T1 | Redenumirea fisierelor care respecta un sablon dat
Cerinta: Dezvoltati un script ce redenumeste toate fisierele de tip jpeg dintr-un folder specificat

Surse:
https://stackoverflow.com/questions/21697645/how-to-extract-metadata-from-a-image-using-python
https://note.nkmk.me/en/python-opencv-pillow-image-size/
https://www.tutorialspoint.com/How-to-move-a-file-from-one-folder-to-another-using-Python
https://stackoverflow.com/questions/2491222/how-to-rename-a-file-using-python
"""

from PIL import Image
import exifread
import os
import shutil

from utilfunc import p

val = True

while val: #Pentru a putea gasi poza corecta creem un loop infinit!
    try:
        poza = input("Introdu numele pozei (Scrie 'gata' cand nu mai vrei!): ") #Pozele disponibile in director sunt numere de la 10 la 15 inclusiv!
        if poza == "gata": #Conditia de a iesi din loop-ul infinit
            val = False
            continue
        with open(f'Poze/{poza}.jpg', 'rb') as fh: #Deschidem poza selectata
            im = Image.open(f'Poze\{poza}.jpg') #Nu stiu de ce dar nu merge daca nu o deschid si asa?!?!
            tags = exifread.process_file(fh, stop_tag="EXIF DateTimeOriginal") #Extragem data la care a fost facuta poza
            dateTaken = tags["EXIF DateTimeOriginal"] #Variabila in care se afiseaza data
    except FileNotFoundError as e:
        p("Poza aleasa nu exista! Introduceti una existenta!") #In cazul in care nu s-a scris o poza corecta v-a aparea acest mesaj!
    except KeyError:
        p("Aceasta imagine nu are METADATA!!!")
    else:
        p(f'Poza {poza} a fost facuta in data: ', dateTaken)   # AFISARE!
        p(f'Poza {poza} ar dimensiunile: ', im.size)

if not os.path.exists('Poze_Redenumite'):
    os.mkdir('Poze_Redenumite')  #Creem fisierul nou pentru a stoca pozele!

path, dirs, files = next(os.walk("Poze"))
nr_poze = len(files) #Numaram cate poze avem in fisier in cazul in care se adauga sau se scot!

lista1 = list()
lista2 = list()
for k in range (10,10 + nr_poze):
    im = Image.open(f'Poze/{k}.jpg')
    lista1.append(im.size)
    with open(f'Poze/{k}.jpg', 'rb+') as fh:
        tags = exifread.process_file(fh, stop_tag="EXIF DateTimeOriginal")
        dateTaken = tags["EXIF DateTimeOriginal"]
        data = str(dateTaken)
        date = data[0:4] + " " + data[5:7] + " " + data[8:11]
    catre_fisier_nou = shutil.copy(f'Poze/{k}.jpg', f'Poze_Redenumite/{date}_{k-9}_{k}_{lista1[k-10]}.jpg')
