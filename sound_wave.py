import wave

def valeur_onde_sonore(chemin_fichier, temps):
    # Ouvrir le fichier audio
    fichier_audio = wave.open(chemin_fichier, 'r')

    # Obtenir le taux d'échantillonnage et la durée du fichier audio
    taux_echantillonnage = fichier_audio.getframerate()
    print("taux d'échantillonage : {}".format(taux_echantillonnage))
    duree_audio = fichier_audio.getnframes() / float(taux_echantillonnage)

    # Calculer le nombre d'échantillons à lire à partir du temps donné
    nb_echantillons_a_lire = int(temps * taux_echantillonnage)

    # Déplacer la position de lecture du fichier audio au temps donné
    # fichier_audio.setpos(int(temps * taux_echantillonnage))
    fichier_audio.setpos(6)

    # Lire l'échantillon à la position donnée
    valeur = fichier_audio.readframes(1)
    valeur = int.from_bytes(valeur, byteorder='little', signed=True)

    # Fermer le fichier audio
    fichier_audio.close()

    return valeur

# Exemple d'utilisation de la fonction
chemin_fichier_audio = "HIROSHIMA30_1.wav"
temps_demande = 5.1  # Temps en secondes
valeur = valeur_onde_sonore(chemin_fichier_audio, temps_demande)
print("Valeur de l'onde sonore à {} secondes : {}".format(temps_demande, valeur))
