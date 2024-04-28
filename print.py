import cups
from PIL import Image, ImageDraw
import random
import ewave
import sys
import time

import matplotlib.pyplot as plt
# from matplotlib.animation import FuncAnimation

# soundfile = "HIROSHIMA30_1.wav"
soundfile = "iceland(dematrix).wav"
average_q = 10
offset = 2000 * average_q

# Vérifier le nombre d'arguments
if len(sys.argv) != 2:
    print("Usage: python3 script.py loopQ")
    sys.exit(1)

# Récupérer les arguments
dots = int(sys.argv[1]) #nb de points a imprimer

def generer_image(largeur, hauteur, taille_carre, position):
    # Création de l'image avec fond blanc et résolution de 300 PPI
    image = Image.new("RGB", (largeur, hauteur), "white")
    image.info['dpi'] = (300, 300)

    # Dessin d'un carré noir à une position aléatoire
    # x = random.randint(0, largeur - taille_carre)
    # Dessin d'un carré noir à la position transmise par la fonction
    x = position
    y = 0
    draw = ImageDraw.Draw(image)
    # draw.rectangle([0, 0, largeur, hauteur], fill="black")
    draw.rectangle([x, y, x + taille_carre, y + taille_carre], fill="black")
    image.save("image.png", dpi=(300, 300))

    # return image

def get_sample(file):
    with ewave.open(file) as w:
        print("samplerate = {0.sampling_rate} Hz, length = {0.nframes} samples, "
              "channels = {0.nchannels}, dtype = {0.dtype!r}".format(w))
        data = w.read()
        return data
    
def scale(valeur, valeur_min, valeur_max, echelle_min, echelle_max):
    # Calcul de la valeur mise à l'échelle
    valeur_echelle = (valeur - valeur_min) * (echelle_max - echelle_min) / (valeur_max - valeur_min) + echelle_min
    return int(valeur_echelle)

def average(data, location, q):
    #moyenne de q points
    average = 0
    for x in range(q):
        average += data[location + x + offset, 0]
        # print("data {} = {}".format(x + location, data[location + x, 0]))
        # print("average++ =", average)
    average /= q
    return int(average)

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
for x in range(dots):
    # level = scale(data[x * 10, 0], -32768, 32767, 0, 844)
    # print("total average=", average(data, average_q * x, average_q))
    level = scale(average(data, average_q * x, average_q), -32768, 32767, 0, 844)
    print("level =", level)
    generer_image(850, 6, 6, level)
    # show_image()
    job_id = conn.printFile(epson, dot_pict, "Titre du travail", options)
    print("Travail d'impression envoyé avec l'ID:", job_id)
    while True:
        # Vérifier le statut du travail
        job_attributes = conn.getJobAttributes(job_id)
        job_state = job_attributes['job-state']
        # print("job state=", job_state)
        time.sleep(0.1)
        if job_state == 9:
                break
