import cups
from PIL import Image, ImageDraw
import random
import ewave

soundfile = "HIROSHIMA30_1.wav"
def generer_image(largeur, hauteur, taille_carre):
    # Création de l'image avec fond blanc et résolution de 300 PPI
    image = Image.new("RGB", (largeur, hauteur), "white")
    image.info['dpi'] = (300, 300)

    # Dessin d'un carré noir à une position aléatoire
    x = random.randint(0, largeur - taille_carre)
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
    

# generer_image(850, 8, 8)  # Générer une image de 850x8 pixels avec un carré noir de 8x8 pixels
# Sauvegarde de l'image en PNG

# Connexion à CUPS
conn = cups.Connection()

# Récupérer l'imprimante par défaut
printer = conn.getDefault()
epson = "EPSON_TM_T88V"

# Imprimer un fichier
texte = "/Users/r/Desktop/mud/test_print_c/text.txt"  # Remplacez par le chemin de votre fichier
image = "pixel_850x8px.png"
random_pics = "image.png"

options = {
    'fit-to-page': 'letter',  # Ajustement à la page (peut être différent selon la taille de votre papier)
    # 'media': 'continuous'  # Papier continu
}
data = get_sample(soundfile)
for x in range(1000):
    generer_image(850, 6, 6)
    job_id = conn.printFile(epson, random_pics, "Titre du travail", options)
    print("Travail d'impression envoyé avec l'ID:", job_id)
    print("data =", data[x, 0])
