import tempfile
import os
import shutil
import glob
import requests
import zipfile
from bs4 import BeautifulSoup

# ===== PARAMETRES

Path_Installation = "c:\\tools\\Putty\\"
Software_Url = "https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html"
Software_Latest_Binaries="https://the.earth.li/~sgtatham/putty/latest/w64/putty.zip"

# =====

File_Version = "PUTTY_VERSION.TXT"

def download_file(url, filename):
    http_response = requests.get(url, stream=True)
    with open(filename, 'wb') as my_file:
        shutil.copyfileobj(http_response.raw, my_file)


def UNZip(ZipFile, PathTarget = ''): 
    if PathTarget == '': PathTarget = os.getcwd()  
    zfile = zipfile.ZipFile(ZipFile, 'r') 
    for i in zfile.namelist():  ## On parcourt l'ensemble des fichiers de l'archive 
        print("Décompression",i)
        if os.path.isdir(i):   ## S'il s'agit d'un repertoire, on se contente de creer le dossier 
            try: os.makedirs(PathTarget + os.sep + i) 
            except: pass 
        else: 
            try: os.makedirs(PathTarget + os.sep + os.path.dirname(i)) 
            except: pass 
            data = zfile.read(i) 
            fp = open(PathTarget + os.sep + i, "wb")  
            fp.write(data)       
            fp.close() 
    zfile.close()   


# Recherche la version
Need_To_Download = False
Current_Version = ''

try:
    with open(Path_Installation + File_Version, "r") as f:
        for line in f.readlines():
            Current_Version=line        
            break
except IOError:
    Current_Version=""
        

if Current_Version == '':
    print('> Impossible de détecter la version installée sur le poste')
else:
    print('> Version installée',Current_Version)    

print("Contact du site de l'éditeur...")
r = requests.get(Software_Url)
if r.status_code != 200:
    print("Error : Impossible de contacter le site de l'éditeur \n",Software_Url,"\n")
    exit(1)
print("> OK")

MySoup = BeautifulSoup(r.text, 'html.parser')
v = MySoup.title.text

Version = v[v.find('(')+1:v.find(')')-1]
print('> Version disponible au téléchargement :',Version)

if Version != Current_Version:
    print('Téléchargement de la nouvelle version')
    download_file(Software_Latest_Binaries, tempfile.gettempdir()+"\\putty.zip")
    print("Décompression des fichiers dans le répertoire d'installation",Path_Installation)
    try:
        os.mkdir(Path_Installation)
    except IOError:
        pass
    UNZip(tempfile.gettempdir()+"\\putty.zip", Path_Installation)
    print("Suppression du download temporaire",tempfile.gettempdir()+"\\putty.zip")
    # On stocke la version installée 

    with open(Path_Installation + File_Version, "w") as f:
        f.write(Version)
        f.close()
        
    os.remove(tempfile.gettempdir()+"\\putty.zip")

else:
    print("La version de Putty est déjà à jour.")

print("Fin de script")    
exit(0)
