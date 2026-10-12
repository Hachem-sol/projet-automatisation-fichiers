# Automatisation de l'organisation des fichiers avec Python

## Présentation

Ce projet est un outil d'automatisation développé en Python qui classe automatiquement les fichiers dans des dossiers selon leur extension.

Il peut également surveiller un dossier pour organiser les nouveaux fichiers, ignorer certains fichiers temporaires et éviter l'écrasement des fichiers en double.

## Fonctionnalités

* Classement automatique des fichiers par catégorie.
* Prise en charge des PDF, images, fichiers Excel, CSV, Word, PowerPoint, fichiers texte, vidéos, fichiers audio et archives.
* Gestion des fichiers sans extension.
* Détection et traitement des doublons sans écraser les fichiers existants.
* Ignorance des fichiers temporaires.
* Surveillance automatique d'un dossier grâce à `watchdog`.
* Journalisation des opérations et des erreurs.
* Tests automatisés avec `pytest`.

## Technologies utilisées

* Python 3
* Watchdog
* Pytest
* Git et GitHub

## Installation

### 1. Cloner le dépôt

```bash
git clone https://github.com/Hachem-sol/projet-automatisation-fichiers.git
cd projet-automatisation-fichiers
```

### 2. Installer les dépendances

```bash
python -m pip install -r requirements.txt
```

## Utilisation

Place les fichiers à organiser dans le dossier `fichiers_test`, puis lance le programme :

```bash
python organiser.py
```

Le programme classe les fichiers dans des sous-dossiers selon leur catégorie.

## Exécuter les tests

Pour lancer les tests automatisés :

```bash
python -m pytest test_pytest.py -v
```

## Structure du projet

```text
projet-automatisation-fichiers/
├── config.py
├── organiser.py
├── requirements.txt
├── test_automatisation.py
├── test_pytest.py
├── .gitignore
└── README.md
```

Les dossiers de test et de journaux sont ignorés par Git conformément au fichier `.gitignore`. Ils peuvent être créés localement pendant l'utilisation du programme.

## Objectif pédagogique et professionnel

Ce projet a été réalisé pour développer mes compétences en Python, automatisation des tâches répétitives, tests logiciels et gestion de versions avec Git.

Il constitue une première étape vers la réalisation de solutions d'automatisation utiles aux particuliers et aux entreprises.

## Auteur

**Hachem-sol**

* GitHub : https://github.com/Hachem-sol
