import pyautogui as pgui
import cv2 as cv

class InteractionInteral():
    def __init__(self):
        # Detail
        self.capture_onglet_detail = "self.captures/Detail.png"
        self.capture_page_detail = "self.captures/PageDetail.png"
        self.capture_detail_no_equipement = "self.captures/NoEquipement.png"
        self.capture_detail_description = "self.captures/Description.png"
        self.capture_detail_poste_comptable = "self.captures/PosteComptable.png"
        self.capture_detail_localisation = "self.captures/Localisation.png"
        self.capture_detail_groupe = "self.captures/Groupe.png"
        self.capture_detail_division = "self.captures/Division.png"

        # Personnalise
        self.capture_onglet_personnalise = "self.captures/Personnalise.png"
        self.capture_page_personnalise = "self.captures/PagePersonnalise.png"
        self.capture_personnalise_nom = "self.captures/PersoNom.png"
        self.capture_personnalise_manufacturier = "self.captures/PersoManu.png"
        self.capture_personnalise_modele = "self.captures/PersoModele.png"
        self.capture_personnalise_no_serie = "self.captures/PersoNoSerie.png"

        # General
        self.capture_onglet_general = "self.captures/General.png"
        self.capture_page_general = "self.captures/PageGeneral.png"
        self.capture_general_manufacturier = "self.captures/GeneralManufacturier.png"
        self.capture_general_modele = "self.captures/GeneralModele.png"
        self.capture_general_no_serie = "self.captures/GeneralNoSerie.png"

        # Autre
        self.capture_x_onglet_actif = "self.captures/xOngletActif.png"
        self.capture_bouton_sauver = "self.captures/Sauver.png"
        self.capture_bouton_sauver_plus = "self.captures/Sauver+.png"

# Affichage des onglets
def afficher_onglet_detail(self):
    InteractionInteral.selectionner_champ(self.capture_onglet_detail)

def afficher_onglet_personnalise(self):
    InteractionInteral.selectionner_champ(self.capture_onglet_personnalise)

def afficher_onglet_general(self):
    InteractionInteral.selectionner_champ(self.capture_onglet_general)

# Selection des champs onglet détail
def selectionner_champ_detail_no_equipement(self):
    InteractionInteral.selectionner_champ(self.capture_detail_no_equipement)

def selectionner_champ_detail_description(self):
    InteractionInteral.selectionner_champ(self.capture_detail_description)

def selectionner_champ_detail_poste_comptable(self):
    InteractionInteral.selectionner_champ(self.capture_detail_poste_comptable, 3)

def selectionner_champ_detail_localisation(self):
    InteractionInteral.selectionner_champ(self.capture_detail_localisation)

def selectionner_champ_detail_groupe(self):
    InteractionInteral.selectionner_champ(self.capture_detail_groupe)

def selectionner_champ_detail_division(self):
    InteractionInteral.selectionner_champ(self.capture_detail_division)

# Selection des champs onglet personnalise
def selectionner_champ_personnalise_nom(self):
    InteractionInteral.selectionner_champ(self.capture_personnalise_nom)

def selectionner_champ_personnalise_manufacturier(self):
    InteractionInteral.selectionner_champ(self.capture_personnalise_manufacturier)

def selectionner_champ_personnalise_modele(self):
    InteractionInteral.selectionner_champ(self.capture_personnalise_modele)

def selectionner_champ_personnalise_no_serie(self):
    InteractionInteral.selectionner_champ(self.capture_personnalise_no_serie)

# Selection des champs onglet general
def selectionner_champ_general_manufacturier(self):
    InteractionInteral.selectionner_champ(self.capture_general_manufacturier)

def selectionner_champ_general_modele(self):
    InteractionInteral.selectionner_champ(self.capture_general_modele)

def selectionner_champ_general_no_serie(self):
    InteractionInteral.selectionner_champ(self.capture_general_no_serie)

# Validations
def valider_ouverture_onglet_detail(self):
    InteractionInteral.valider_onglet_actif(self.capture_page_detail)

def valider_ouverture_onglet_personnalise(self):
    InteractionInteral.valider_onglet_actif(self.capture_page_personnalise)

def valider_ouverture_onglet_general(self):
    InteractionInteral.valider_onglet_actif(self.capture_page_general)

# Autre
def fermer_onglet_actif(self):
    InteractionInteral.selectionner_champ(self.capture_x_onglet_actif)

def sauvegarder_equipement(self):
    InteractionInteral.selectionner_champ(self.capture_bouton_sauver)

def sauvegarder_equipement_et_ouvrir_nouveau(self):
    InteractionInteral.selectionner_champ(self.capture_bouton_sauver_plus)

@staticmethod
def valider_onglet_actif(capture):
    while True:
        if pgui.locateOnScreen(capture, confidence=0.9) is not None:
            return True

@staticmethod
def selectionner_champ(capture, nombre_click=1):
    x, y = pgui.locateCenterOnScreen(capture, confidence=0.9)
    pgui.click(x, y, clicks=nombre_click)






