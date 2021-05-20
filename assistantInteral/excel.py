import openpyxl as pyxl
from openpyxl import cell

class InteractionExcel():
    def __init__(self):
        self.chemin_fichier_principal = "S:/Ingénierie/Administration/Intéral/liste equipement USINE v3.xlsb.xlsx"
        self.chemin_fichier_copie = "équipements ajoutés.xlsx"
        self.wb_principal = pyxl.load_workbook(self.chemin_fichier_principal)
        self.ws_principal = self.wb_principal.worksheets[0]

        self.nom_equipement = ""
        self.rangee_equipement = ""

        self.description_equipement = ""
        self.manufacturier_equipement = ""
        self.modele_equipement = ""
        self.sn_equipement = ""

        self.liste_noms_equipements = []
        for cellule in self.ws_principal["A"]:
            if cellule.value:
                self.liste_noms_equipements.append(cellule.value)

    def trouver_rangee_equipement(self):
        for cellule in self.ws_principal["A"]:
            if cellule.value == self.nom_equipement:
                self.rangee_equipement = str(cellule.row)

    def trouver_colonne_element(self, element):
        for cellule in self.ws_principal["1"]:
            if cellule.value == element:
                return str(chr(ord('@') + cellule.column))

    def trouver_description_equipement(self):
        colonne = self.trouver_colonne_element("Description")
        self.description_equipement = self.ws_principal[colonne + self.rangee_equipement].value

    def trouver_manufacturier_equipement(self):
        colonne = self.trouver_colonne_element("Manufacturier")
        self.manufacturier_equipement = self.ws_principal[colonne + self.rangee_equipement].value

    def trouver_modele_equipement(self):
        colonne = self.trouver_colonne_element("Modèle")
        self.modele_equipement = self.ws_principal[colonne + self.rangee_equipement].value

    def trouver_sn_equipement(self):
        colonne = self.trouver_colonne_element("SN")
        self.sn_equipement = self.ws_principal[colonne + self.rangee_equipement].value

    def produire_texte_informations_equipement(self):
        texte = "{}\n\n{}\n\n{}\n\n{}\n\n{}".format(self.nom_equipement, self.description_equipement, 
                            self.manufacturier_equipement, self.modele_equipement, self.sn_equipement)
        return texte

    def trouver_informations_equipement(self):
        if self.nom_equipement in self.liste_noms_equipements:
            self.trouver_rangee_equipement()
            self.trouver_description_equipement()
            self.trouver_manufacturier_equipement()
            self.trouver_modele_equipement()
            self.trouver_sn_equipement()
        
        else:
            self.nom_equipement = ""
            self.manufacturier_equipement = "Équipement introuvable"
            self.modele_equipement = ""
            self.description_equipement = ""
            self.sn_equipement = ""

