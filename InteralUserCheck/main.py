import os
import openpyxl as pyxl
import pyautogui as agui
from time import sleep
import win32clipboard as clip


def capturer_checkbox(numero_image):
    position_checkbox = (430, 225, 180, 165)
    nom_capture = 'screenshots/capture_checkbox{}.png'.format(numero_image)
    agui.screenshot(nom_capture, region=position_checkbox)
    return nom_capture

def capturer_groupes(numero_image):
    while True:
        position_groupes = (581, 527, 348, 165)
        afficher_onglet_groupes()
        
        if agui.locateOnScreen('capture_page_groupes.png', confidence=0.9) is not None:
            nom_capture = 'screenshots/capture_groupes{}.png'.format(numero_image)
            agui.screenshot(nom_capture, region=position_groupes)
            return nom_capture

def afficher_onglet_detail():
    agui.click(160, 205)

def afficher_onglet_groupes():
    agui.click(500, 205)

def copier_selection():
    agui.hotkey('ctrl', 'c')
    

def obtenir_selection_texte():
    sleep(1)
    copier_selection()
    clip.OpenClipboard(0)
    selection = clip.GetClipboardData()
    clip.CloseClipboard()
    return selection

def obtenir_champs_utilisateur():
    while True:
        if agui.locateOnScreen('capture_page_detail.png', confidence=0.9) is not None:
            numero = obtenir_selection_texte()
            print(numero)
            agui.hotkey('tab')
            prenom = obtenir_selection_texte()
            print(prenom)
            agui.hotkey('tab')
            nom = obtenir_selection_texte()
            print(nom)
            return numero, prenom, nom

def definir_nom_utilisateur():
    numero, prenom, nom = obtenir_champs_utilisateur()
    print(numero, prenom, nom)
    return '{} - {} {}'.format(numero, prenom, nom)

def ouvrir_page_utilisateur():
    agui.hotkey('return')

def fermer_page_utilisateur():
    agui.hotkey('esc')

def passer_au_prochain_utilisateur():
    while True:
        if agui.locateOnScreen('capture_page_liste.png', confidence=0.9) is not None:
            agui.hotkey('down')
            return

def inserer_nom_utilisateur_dans_fichier(fichier, colonne, rangee, valeur):
    feuille = fichier.active
    feuille[colonne + rangee] = valeur
    feuille[colonne + rangee].alignment = pyxl.styles.Alignment(vertical='center')
    
    feuille.column_dimensions[colonne].width = 25.00
    fichier.save('Liste acces Interal.xlsx')

def inserer_image_dans_fichier(fichier, colonne, rangee, capture, largeur):
    feuille = fichier.active
    image = pyxl.drawing.image.Image(capture)
    image.anchor = colonne + rangee
    feuille.add_image(image)
    feuille.column_dimensions[colonne].width = largeur
    feuille.row_dimensions[int(rangee)].height = 125.00
    fichier.save('Liste acces Interal.xlsx')

def obtenir_informations_utilisateur(limite=1000):
    utilisateurs = []
    agui.click(5, 5)
    fichier = pyxl.Workbook()
    i = 0
    while True:
        if i % 2 == 0:
            rangee = str(i + 1)
            ouvrir_page_utilisateur()
            nom = definir_nom_utilisateur()

            if nom not in utilisateurs:
                inserer_nom_utilisateur_dans_fichier(fichier, 'A', rangee, nom) 

                capture_checkbox = capturer_checkbox(i)
                inserer_image_dans_fichier(fichier, 'B', rangee, capture_checkbox, 25.00)

                capture_groupes = capturer_groupes(i)
                inserer_image_dans_fichier(fichier, 'C', rangee, capture_groupes, 50.00)

                fermer_page_utilisateur()
                passer_au_prochain_utilisateur()
                utilisateurs.append(nom)

            elif nom in utilisateurs or i == limite * 2:
                break
        i += 1

if __name__ == "__main__":
    obtenir_informations_utilisateur(5)
