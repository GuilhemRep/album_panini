# -*- coding: utf-8 -*-

from PIL import Image, ImageFilter, ImageDraw, ImageFont
import os, sys
from fpdf import FPDF

# Fonction déterminant le prénom associé à une image
def prenom(image):
    nom=[i for i in image]
    fin=0
    while nom[fin]!='.':
        fin+=1
    debut=fin
    while nom[debut]!='/':
        debut-=1
    prenom=''
    debut+=1
    if ord(nom[debut])>=97 and ord(nom[debut])<=122:
        nom[debut]=chr(ord(nom[debut])-32)
    for i in range(debut,fin):
        prenom+=nom[i]
    # Pour les accents et autres caractères étranges (apparement OK à partir de python 3.8)
    #prenom = unicode(prenom,'utf-8')
    return prenom
    
# Chemin du dossier
path = '/home/guilhem/Desktop/Python/disney'

# Chemin des logos
HX = Image.open(path+'/HX.png')
HX_trans = Image.open(path+'/HX_trans.png')

# PDF
pdf = FPDF()

# Police
fnt = ImageFont.truetype(path+'/font/timeburnernormal.ttf',130)

# Liste des images
files = []
# r=root, d=directories, f = files
for r, d, f in os.walk(path+'/images'):
    for file in f:
        if '.jpg' or '.jpeg' in file:
            files.append(os.path.join(r, file))

TINT_COLOR = (0, 0, 0)
TRANSPARENCY = .75
OPACITY = int(255 * TRANSPARENCY)

print("Traitement en cours :")

for i in range(len(files)):
    nom=prenom(files[i])
    print("->",nom)
    
    # Accentuation de l'image + redimensionement
    img = Image.open(files[i])
    #img = img.filter(ImageFilter.SHARPEN)
    img = img.resize((827,int((img.size[1]*827/img.size[0]))),Image.ANTIALIAS)
    
    # Zone de "dessin"
    draw = ImageDraw.Draw(img)
    # Pour la transparence
    img = img.convert("RGBA")
    
    # Dimensions de l'image et du texte à incruster
    W,H=(img.size[0],img.size[1])
    w,h = draw.textsize(nom, font=fnt)
    
    overlay = Image.new('RGBA', img.size)
    draw = ImageDraw.Draw(overlay)
    
    # Rectangle transparent haut-gauche, bas-droite
    draw.rectangle((0, H-180, W, H), fill=TINT_COLOR+(OPACITY,))
    
    img = Image.alpha_composite(img, overlay)
    
    # Ecriture du prénom ((gauche,haut),nom,couleur,police)
    draw = ImageDraw.Draw(img)
    draw.text(((W-w+HX.size[0])/2,H-173),nom,(255,255,255),font=fnt)
    img.paste(HX, (0,H-180), mask=HX_trans)
    
    # On repasse en RGB pour le format jpeg
    img = img.convert("RGB")
    nom_image=path+'/images_ok/'+nom+'_ok.jpg'
    img.save(nom_image)
    
    # Nouvelle page pdf
    pdf.add_page()
    img=img.rotate(180)
    pdf.image(nom_image, x=10, y=15,w=W/4.35,h=H/4.35)
    print(img.size)

nombre_photos=str(len(files))
pdf.output(path+"/images_ok/Fichier_imprimable_("+nombre_photos+"_personnages).pdf")
print("Terminé !")