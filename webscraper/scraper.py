from bs4 import BeautifulSoup
import requests

class Scraper():
    def __init__(self):
        self.page = requests.get('https://www.ulaval.ca/etudes/programmes/baccalaureat-en-informatique#section-structure')
        self.soup = BeautifulSoup(self.page.content, 'html.parser')

        self.liste_sections = self.etablir_liste_sections()

        self.section_principale = self.liste_sections[0]
        self.section_autre = self.liste_sections[1]

        self.liste_toggles_section_principale = self.etablir_liste_toggles(self.section_principale) 
        self.liste_toggles_section_autre = self.etablir_liste_toggles(self.section_autre) 

        #self.liste_cours_section_principale = []
        #self.liste_cours_section_autre = []

        self.liste_cours_section_principale = self.etablir_liste_cours(self.liste_toggles_section_principale)
        self.liste_cours_section_autre = self.etablir_liste_cours(self.liste_toggles_section_autre)

        """for toggle in self.liste_toggles_section_principale:
            self.liste_cours_section_principale.append(self.etablir_liste_cours(toggle))

        for toggle in self.liste_toggles_section_autre:
            self.liste_cours_section_autre.append(self.etablir_liste_cours(toggle))"""


    def etablir_liste_sections(self):
        structure = self.soup.find("section", id="section-structure")
        return structure.find_all("div", class_="fe-bloc-section")[:2]

    def trouver_nom_section(self, section):
        return section.find("h4", class_="fe-bloc-titre--texte").text.strip()

    def etablir_liste_toggles(self, section):
        return section.find_all("div", class_="toggle-section")

    def trouver_nom_toggle(self, toggle):
        return toggle.find("span", class_="item").text.strip("parmi :")

    def etablir_liste_cours(self, liste_toggles):
        liste_cours = []
        for toggle in liste_toggles:
            liste_cours.append(toggle.find_all("a", class_="carte-accessible--lien"))
        return liste_cours
        
    def trouver_url_cours(self, cours):
        return "https://www.ulaval.ca/{}".format(cours["href"])

    def trouver_informations_cours(self, cours):
        url = self.trouver_url_cours(cours)
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        div = soup.find("div", class_="c-grid")

        numero = div.find("span", class_="fe--titre-type").text
        titre = div.find("span", class_="fe--titre-nom").text
        nombre_credits = div.find("span", class_="promo-entete--titre").text
        horaire = "Information indisponible"

        contenu = div.find_all("ul", class_="promo-entete--contenu")
        if len(contenu) > 2:
            horaire = contenu[2].text

        return numero, titre, nombre_credits, horaire


if __name__ == "__main__":
    scraper = Scraper()
    for sous_liste_cours in scraper.liste_cours_section_principale:
        for cours in sous_liste_cours:
            print(scraper.trouver_informations_cours(cours))

    for sous_liste_cours in scraper.liste_cours_section_autre:
        for cours in sous_liste_cours:
            print(scraper.trouver_informations_cours(cours))


