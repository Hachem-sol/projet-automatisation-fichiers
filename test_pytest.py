from organiser import determiner_categorie


def test_extension_pdf():
    assert determiner_categorie(".pdf") == "PDF"


def test_extension_inconnue():
    assert determiner_categorie(".xyz") == "Autres"

def test_extension_image():
    assert determiner_categorie(".jpg") == "Images"


def test_extension_excel():
    assert determiner_categorie(".xlsx") == "Excel"

   
import organiser
from pathlib import Path


def test_deplacement_fichier_pdf(tmp_path, monkeypatch):
    # Utilise un dossier temporaire pour ne pas toucher aux vrais fichiers
    monkeypatch.setattr(organiser, "dossier", str(tmp_path))

    # Cree un fichier PDF de test
    fichier = tmp_path / "rapport_test.pdf"
    fichier.write_text("Contenu de test", encoding="utf-8")

    # Lance l'organisation du fichier
    organiser.organiser_fichier(str(fichier))

    # Verifie que le fichier a ete deplace dans le dossier PDF
    destination = tmp_path / "PDF" / "rapport_test.pdf"
    assert destination.exists()

    # Verifie que le fichier original n'existe plus a son emplacement initial
    assert not fichier.exists() 

    
def test_deplacement_fichier_sans_extension(tmp_path, monkeypatch):
    # Utilise un dossier temporaire pour le test
    monkeypatch.setattr(organiser, "dossier", str(tmp_path))

    # Cree un fichier sans extension
    fichier = tmp_path / "README_TEST"
    fichier.write_text("Contenu de test", encoding="utf-8")

    # Lance l'organisation
    organiser.organiser_fichier(str(fichier))

    # Verifie que le fichier est dans la bonne categorie
    destination = tmp_path / "Sans_extension" / "README_TEST"
    assert destination.exists()

    # Verifie que le fichier a quitte son emplacement initial
    assert not fichier.exists()

    
def test_fichier_temporaire_ignore(tmp_path, monkeypatch):
    # Utilise un dossier temporaire
    monkeypatch.setattr(organiser, "dossier", str(tmp_path))

    # Cree un fichier temporaire
    fichier = tmp_path / "temp_test.tmp"
    fichier.write_text("Fichier temporaire", encoding="utf-8")

    # Lance l'organisation
    organiser.organiser_fichier(str(fichier))

    # Verifie que le fichier est toujours a sa place
    assert fichier.exists()

    # Verifie qu'aucun dossier de categorie n'a ete cree
    assert not (tmp_path / "Autres").exists()

    
def test_fichier_office_temporaire_ignore(tmp_path, monkeypatch):
    # Utilise un dossier temporaire pour le test
    monkeypatch.setattr(organiser, "dossier", str(tmp_path))

    # Cree un fichier temporaire Office
    fichier = tmp_path / "~$document.docx"
    fichier.write_text("Fichier temporaire Office", encoding="utf-8")

    # Lance l'organisation
    organiser.organiser_fichier(str(fichier))

    # Verifie que le fichier est toujours a sa place
    assert fichier.exists()

    # Verifie qu'aucun dossier Word n'a ete cree
    assert not (tmp_path / "Word").exists()

    
def test_doublon_pdf_sans_ecrasement(tmp_path, monkeypatch):
    # Utilise un dossier temporaire pour le test
    monkeypatch.setattr(organiser, "dossier", str(tmp_path))

    # Cree le dossier PDF et un fichier qui existe deja
    dossier_pdf = tmp_path / "PDF"
    dossier_pdf.mkdir()
    fichier_existant = dossier_pdf / "rapport.pdf"
    fichier_existant.write_text("Ancien contenu", encoding="utf-8")

    # Cree un nouveau fichier portant le meme nom
    nouveau_fichier = tmp_path / "rapport.pdf"
    nouveau_fichier.write_text("Nouveau contenu", encoding="utf-8")

    # Lance l'organisation
    organiser.organiser_fichier(str(nouveau_fichier))

    # Verifie que le fichier existant n'a pas ete ecrase
    assert fichier_existant.read_text(encoding="utf-8") == "Ancien contenu"

    # Verifie que le nouveau fichier a ete conserve sous un autre nom
    doublon = dossier_pdf / "rapport_1.pdf"
    assert doublon.exists()
    assert doublon.read_text(encoding="utf-8") == "Nouveau contenu"

    
def test_fichier_inexistant_ne_provoque_pas_erreur(tmp_path, monkeypatch):
    # Utilise un dossier temporaire
    monkeypatch.setattr(organiser, "dossier", str(tmp_path))

    # Definir un chemin vers un fichier inexistant
    fichier = tmp_path / "inexistant.pdf"

    # Appeler la fonction ne doit pas provoquer d'exception
    organiser.organiser_fichier(str(fichier))

    # Verifier que le fichier n'a pas ete cree
    assert not fichier.exists()