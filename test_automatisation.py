# -*- coding: utf-8 -*-

from organiser import determiner_categorie


# Test 1 : une extension connue
resultat = determiner_categorie(".pdf")

if resultat == "PDF":
    print("TEST 1 OK : PDF")
else:
    print("TEST 1 ERREUR")


# Test 2 : une extension inconnue
resultat = determiner_categorie(".xyz")

if resultat == "Autres":
    print("TEST 2 OK : Autres")
else:
    print("TEST 2 ERREUR")
	
import os
import shutil
import organiser


# Dossier utilisé uniquement pour les tests
organiser.dossier = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "tests_fichiers"
)

# Test 3 : organisation réelle d'un fichier PDF
organiser.organiser_fichier("test.pdf")

# Vérifie que le fichier a été déplacé dans le dossier PDF
fichier_deplace = os.path.join(
    organiser.dossier,
    "PDF",
    "test.pdf"
)

if os.path.exists(fichier_deplace):
    print("TEST 3 OK : fichier PDF deplace")
else:
    print("TEST 3 ERREUR : fichier PDF non deplace")
	
	# Test 4 : fichier sans extension
organiser.organiser_fichier("README_TEST")

fichier_sans_extension = os.path.join(
    organiser.dossier,
    "Sans_extension",
    "README_TEST"
)

if os.path.exists(fichier_sans_extension):
    print("TEST 4 OK : fichier sans extension deplace")
else:
    print("TEST 4 ERREUR : fichier sans extension non deplace")
	
	# Test 5 : fichier temporaire ignore
organiser.organiser_fichier("temp_test.tmp")

fichier_temporaire = os.path.join(
    organiser.dossier,
    "temp_test.tmp"
)

if os.path.exists(fichier_temporaire):
    print("TEST 5 OK : fichier temporaire ignore")
else:
    print("TEST 5 ERREUR : fichier temporaire deplace")
	
	# Test 6 : fichier temporaire Word ignore
organiser.organiser_fichier("~$document.docx")

fichier_word_temporaire = os.path.join(
    organiser.dossier,
    "~$document.docx"
)

if os.path.exists(fichier_word_temporaire):
    print("TEST 6 OK : fichier ~$ ignore")
else:
    print("TEST 6 ERREUR : fichier ~$ deplace")
	
	
	# Test 7 : gestion des doublons
organiser.organiser_fichier("test.pdf")

fichier_original = os.path.join(
    organiser.dossier,
    "PDF",
    "test.pdf"
)

fichier_doublon = os.path.join(
    organiser.dossier,
    "PDF",
    "test_1.pdf"
)

if os.path.exists(fichier_original) and os.path.exists(fichier_doublon):
    print("TEST 7 OK : doublon gere sans ecraser")
else:
    print("TEST 7 ERREUR : probleme de gestion du doublon")
	
	
	# Test 8 : gestion d'une erreur
organiser.organiser_fichier("fichier_inexistant.pdf")

print("TEST 8 TERMINE : gestion de l'erreur verifiee")