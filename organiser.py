import os                                      # Gestion des fichiers et dossiers
import shutil                                  # Déplacement des fichiers
import time                                    # Pause du programme
import logging                                 # Système de journalisation

dossier_logs = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "logs"
)

os.makedirs(dossier_logs, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(dossier_logs, "automatisation.log"),        # Fichier où seront enregistrés les événements
    level=logging.INFO,                        # Enregistre les informations importantes
    format="%(asctime)s | %(levelname)s | %(message)s"  # Format du journal
)

from watchdog.observers import Observer        # Surveillance du dossier
from watchdog.events import FileSystemEventHandler  # Gestion des événements

from config import (
    categories,             # Importe les catégories depuis config.py
    extensions_ignorees,    # Importe les extensions_ignorees
    prefixes_ignores,       # Importe les prefixes_ignores
    categorie_sans_extension,# Importe categorie_sans_extension
    dossier_a_surveiller      # Importe dossier_a_surveiller
)                 



logger = logging.getLogger(__name__)           # Crée notre journal

dossier = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    dossier_a_surveiller
)                   


def determiner_categorie(extension):            # Détermine la catégorie
    return categories.get(extension, "Autres")  # Retourne la catégorie


def deplacer_fichier(fichier, categorie):       # Déplace un fichier

    chemin_fichier = os.path.join(dossier, fichier)  # Chemin du fichier

    chemin_categorie = os.path.join(dossier, categorie)  # Dossier destination

    if not os.path.exists(chemin_categorie):    # Vérifie si le dossier existe
        os.makedirs(chemin_categorie)            # Crée le dossier

    destination = os.path.join(chemin_categorie, fichier)  # Destination initiale

    if os.path.exists(destination):              # Vérifie si le nom existe déjà

        nom, extension = os.path.splitext(fichier)  # Sépare le nom et l'extension

        compteur = 1                              # Commence le compteur

        while True:                               # Cherche un nom disponible

            nouveau_nom = f"{nom}_{compteur}{extension}"  # Nouveau nom

            nouvelle_destination = os.path.join(
                chemin_categorie,
                nouveau_nom
            )

            if not os.path.exists(nouvelle_destination):  # Nom disponible
                destination = nouvelle_destination         # Utilise ce nom
                break                                      # Arrête la recherche

            compteur += 1                         # Passe au numéro suivant

    shutil.move(chemin_fichier, destination)       # Déplace le fichier

    return destination                            # Retourne le vrai chemin

def fichier_pret(chemin_fichier):                # Vérifie si la copie est terminée

    taille_precedente = -1                       # Ancienne taille du fichier

    for tentative in range(5):                   # Vérifie jusqu'à 5 fois

        if not os.path.exists(chemin_fichier):   # Vérifie que le fichier existe
            return False                         # Fichier introuvable

        taille_actuelle = os.path.getsize(chemin_fichier)  # Taille actuelle

        if taille_actuelle == taille_precedente: # La taille ne change plus
            return True                          # Le fichier est prêt

        taille_precedente = taille_actuelle     # Mémorise la nouvelle taille

        time.sleep(1)                            # Attend 1 seconde

    return False                                 # Le fichier semble encore occupé	

def organiser_fichier(fichier):                  # Organise un fichier

    try:                                         # Essaie d'exécuter le traitement

        chemin_fichier = fichier if os.path.isabs(fichier) else os.path.join(dossier, fichier)  # Chemin complet

        if not os.path.isfile(chemin_fichier):   # Vérifie que c'est bien un fichier
            return                               # Ignore les dossiers

        if not fichier_pret(chemin_fichier):    # Vérifie que la copie est terminée
            print(f"{fichier} : fichier encore en cours de copie")
            return

        nom_fichier = os.path.basename(chemin_fichier)   # Sépare nom et extension
        nom, extension = os.path.splitext(nom_fichier)

        extension = extension.lower()                # Convertit l'extension en minuscules

        if extension in extensions_ignorees:          # Vérifie si l'extension doit être ignorée
            print(f"{fichier} → fichier ignoré")
            logger.info(f"{fichier} → fichier ignoré")
            return

        for prefixe in prefixes_ignores:              # Vérifie les préfixes interdits

            if os.path.basename(chemin_fichier).startswith(prefixe):           # Vérifie le début du nom
                print(f"{fichier} → fichier ignoré")
                logger.info(f"{fichier} → fichier ignoré")
                return

        if extension == "":
            categorie = categorie_sans_extension
        else:
            categorie = determiner_categorie(extension)   # Détermine la catégorie

        destination = deplacer_fichier(nom_fichier, categorie)  # Déplace et récupère le vrai chemin

        print(f"{fichier} → {categorie}")                    # Affiche le résultat

        logger.info(f"{fichier} → {categorie} → {destination}")  # Enregistre le vrai chemin

    except Exception as erreur:                   # Capture une erreur éventuelle

        print(f"Erreur avec {fichier} : {erreur}") # Affiche l'erreur

        logger.error(f"Erreur avec {fichier} : {erreur}")  # Enregistre l'erreur


class GestionnaireFichiers(FileSystemEventHandler):  # Gestionnaire watchdog

    def on_created(self, event):                 # Appelé lorsqu'un élément est créé

        if event.is_directory:                   # Vérifie si c'est un dossier
            return                               # Ignore les dossiers

        fichier = os.path.basename(event.src_path)  # Récupère le nom du fichier

        organiser_fichier(fichier)               # Organise le nouveau fichier


if __name__ == "__main__":

    event_handler = GestionnaireFichiers()        # Crée le gestionnaire

    observer = Observer()                         # Crée l'observateur

    observer.schedule(                            # Configure la surveillance
        event_handler,                            # Gestionnaire des événements
        dossier,                                  # Dossier à surveiller
        recursive=False                           # Pas de sous-dossiers
    )

    observer.start()                              # Démarre la surveillance

    print("Surveillance du dossier en cours...") # Message de démarrage

    try:
        while True:                               # Maintient le programme actif
            time.sleep(1)                         # Attend 1 seconde

    except KeyboardInterrupt:
        observer.stop()                           # Arrête la surveillance

    observer.join()                               # Attend l'arrêt complet