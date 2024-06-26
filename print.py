import cups
from PIL import Image, ImageDraw
import random
import ewave
import sys
import time
import tempfile

import matplotlib.pyplot as plt
# from matplotlib.animation import FuncAnimation

# soundfile = "HIROSHIMA30_1.wav"
soundfile = "iceland(dematrix).wav"
sampleStep = 1000
offset = 3000 * sampleStep
previous_level = 0
draw_line = True # if false, draw dots
printOrNot = True # False if test mode, without printer attached
showImage = False
lineWidth = 3 # printed line width
getAverage = False # False means pickup raw sample value each sampleStep
currentDot = 0
totalSample = 0

# Vérifier le nombre d'arguments
if len(sys.argv) < 2:
    print("Usage: python3 script.py loopQ average")
    sys.exit(1)
elif (len(sys.argv) == 3):
    if (sys.argv[2] == "average"):
        getAverage = True

# Récupérer les arguments
dots = int(sys.argv[1]) #nb de points a imprimer

def generer_image(largeur, hauteur, taille_carre, position, current_image):
    # Création de l'image avec fond blanc et résolution de 300 PPI
    global previous_level
    image = Image.new("RGB", (largeur, hauteur), "white")
    image.info['dpi'] = (300, 300)
    if current_image == 0:
        previous_level = int(largeur / 2)
    print("previous level= ", previous_level)
    current_level = position
    print("current level= ", current_level)
    draw = ImageDraw.Draw(image)
    if draw_line:
        draw.line([previous_level, 0, current_level, hauteur], fill="black", width=lineWidth)
        # draw.line([0, hauteur, 100, 0], fill="black", width=lineWidth)
        # draw.line([100, hauteur, 0, 0], fill="black", width=lineWidth)
    else:
        # Dessin d'un carré noir à la position transmise par la fonction
        x = position
        y = 0
        draw.rectangle([x, y, x + taille_carre, y + taille_carre], fill="black")
    image.save("image.png", dpi=(300, 300))
    previous_level = current_level

    # return image

def get_sample(file):
    global totalSample
    with ewave.open(file) as w:
        print("samplerate = {0.sampling_rate} Hz, length = {0.nframes} samples, "
              "channels = {0.nchannels}, dtype = {0.dtype!r}".format(w))
        totalSample = w.nframes
        data = w.read()
        return data
    
def scale(valeur, valeur_min, valeur_max, echelle_min, echelle_max):
    # Calcul de la valeur mise à l'échelle
    valeur_echelle = (valeur - valeur_min) * (echelle_max - echelle_min) / (valeur_max - valeur_min) + echelle_min
    return int(valeur_echelle)

# average method
def average(data, location, q):
    #moyenne de q points
    average = 0
    for x in range(q):
        average += data[location + x + offset, 0]
        # print("data {} = {}".format(x + location, data[location + x, 0]))
        # print("average++ =", average)
    average /= q
    return int(average)

# which method used
def getMethod():
     if getAverage:
        return("average")
     else:
        return("jump")

# total printing duration elapsed
def getPrintDuration():
    totalPrintDur = printFinishTime - printStartTime
    m, s = divmod(totalPrintDur, 60)
    return ("{}m{}s".format(int(m), int(s)))

def show_image():
     # Afficher l'image
    display = Image.open(dot_pict)
    plt.imshow(display)
    # plt.axis('off')  # Masquer les axes
    plt.show()

# Connexion à CUPS
conn = cups.Connection()

# Récupérer l'imprimante par défaut
printer = conn.getDefault()
# ici on specifie qu on veut la TM-T88V
epson = "EPSON_TM_T88V"

# Imprimer un fichier
texte = "/Users/r/Desktop/mud/test_print_c/text.txt" # pour test, avec default font
# image = "pixel_850x8px.png"
dot_pict = "image.png"

options = {
    'fit-to-page': 'letter',  # Ajustement à la page (peut être différent selon la taille de votre papier)
    # 'media': 'continuous'  # Papier continu (nb: ne fonctionne pas)
}
data = get_sample(soundfile)
if getAverage:
        print("methode= Average\n")
else:
        print("methode= Pick sample\n")
        
totalDurationM, totalDurationS = divmod(totalSample / 48000, 60)
header = "sampleStep={}\ndots/lines to print={}\noffset={}\nmethod={}\nprint length(S)={}\ntotal length={}m{}s\n\n\n".format(sampleStep, dots, offset, getMethod(), round(sampleStep * dots / 48000, 2), int(totalDurationM), int(totalDurationS))

with tempfile.NamedTemporaryFile(mode='w', delete=False) as fichier_temp:
    fichier_temp.write(header)

# Obtention du nom de fichier temporaire
nom_fichier_temp = fichier_temp.name

# Options d'impression
options_impression = {
    "cpi": "18",
    "lpi": "8",
    # "page-left": "72",
    # "page-top": "72",
    "justify": "left"  # Justification à gauche / not weorking
}

# Impression du fichier temporaire
impression = conn.printFile(epson, nom_fichier_temp, "impression_python.txt", options_impression)
import os
os.remove(nom_fichier_temp)

printStartTime = time.time()
for x in range(dots):
    # level = scale(data[x * 10, 0], -32768, 32767, 0, 844)
    # print("total average=", average(data, sampleStep * x, sampleStep))
    if getAverage:
        level = scale(average(data, sampleStep * x, sampleStep), -32768, 32767, 0, 844)
    else:
        level = scale(data[sampleStep * x + offset, 0], -32768, 32767, 0, 844)
    print("level =", level)
    generer_image(850, 6, 6, level, x)
    if showImage:
        show_image()
    if printOrNot:
        job_id = conn.printFile(epson, dot_pict, "Titre du travail", options)
        print("Travail d'impression envoyé avec l'ID:", job_id)
    while printOrNot:
        # Vérifier le statut du travail
        job_attributes = conn.getJobAttributes(job_id)
        job_state = job_attributes['job-state']
        # print("job state=", job_state)
        time.sleep(0.1)
        if job_state == 9:
                break
    print("Print {}/{}".format(currentDot, dots - 1))
    currentDot += 1
printFinishTime = time.time()
footer = "sampleStep={}\ndots/lines to print={}\noffset={}\nmethod={}\nprint length(S)={}\ntotal length={}m{}s\njob duration(S):{}\n\n".format(sampleStep, dots, offset, getMethod(), round(sampleStep * dots / 48000, 2), int(totalDurationM), int(totalDurationS), getPrintDuration())
with tempfile.NamedTemporaryFile(mode='w', delete=False) as fichier_temp:
    fichier_temp.write(footer)

# Obtention du nom de fichier temporaire
nom_fichier_temp = fichier_temp.name

# Impression du fichier temporaire
impression = conn.printFile(epson, nom_fichier_temp, "impression_python.txt", options_impression)
import os
os.remove(nom_fichier_temp)
