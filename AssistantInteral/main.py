from tkinter import Tk, Frame, Label, Button, Entry, StringVar
from excel import InteractionExcel

class Fenetre(Tk):
    def __init__(self):
        super().__init__()
        self.LARGEUR, self.HAUTEUR = 800, 300
        self.geometry("{}x{}".format(self.LARGEUR, self.HAUTEUR))
        self.resizable(0, 0)

        self.frame = FramePrincipal(self)
        self.frame.grid(row=0, column=0)


class FramePrincipal(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.LARGEUR, self.HAUTEUR = parent.LARGEUR, parent.HAUTEUR
        self["width"], self["height"] = self.LARGEUR, self.HAUTEUR
        self.font_label = ("Courier", 11)
        self.font_bouton = ("Courier", 14)
        self.excel = InteractionExcel()
        
        self.frame_gauche = FrameGauche(self)
        self.frame_gauche.grid(row=0, column=0)

        self.frame_droite = FrameDroite(self)
        self.frame_droite.grid(row=0, column=1)
        

    def trouver_informations_equipement(self):
        self.excel.nom_equipement = self.frame_gauche.entry.get().upper()
        self.frame_gauche.entry.delete(0, "end")
        self.excel.trouver_informations_equipement()
        self.mettre_a_jour_label_informations_equipement()

    def mettre_a_jour_label_informations_equipement(self):
        self.frame_droite.informations_equipement.set(self.excel.produire_texte_informations_equipement())
        

class FrameGauche(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self["width"], self["height"] = 0.25 * parent.LARGEUR, parent.HAUTEUR
        self["borderwidth"], self["relief"] = 2, "raised"

        self.label = Label(self, text="Nom de l'équipement", font=parent.font_label)
        self.label.grid(row=0, column=0, sticky="s")

        self.entry = Entry(self, font=parent.font_label)
        self.entry.grid(row=1, column=0)

        self.bouton_chercher = Button(self, text="Chercher", command=parent.trouver_informations_equipement, 
                             font=parent.font_bouton)
        self.bouton_chercher.grid(row=2, column=0)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_propagate(0)


class FrameDroite(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self["width"], self["height"] = 0.75 * parent.LARGEUR, parent.HAUTEUR
        self["borderwidth"], self["relief"] = 2, "raised"

        self.informations_equipement = StringVar()
        self.label_informations_equipement = Label(self, textvariable=self.informations_equipement, 
                                                   width=55, height=10, font=parent.font_label, justify="left")
        self.label_informations_equipement.grid(row=0, column=1)

        self.label_titre = Label(self, text="Nom\n\nDescription\n\nManufacturier\n\nModèle\n\nSN", 
                                 width=15, height=10, font=parent.font_label, justify="left")
        self.label_titre.grid(row=0, column=0)

        self.bouton_integrer = Button(self, text="Intégrer", font=parent.font_bouton)
        self.bouton_integrer.grid(row=1, column=0, columnspan=2, sticky="n")

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_propagate(0)


if __name__ == "__main__":
    fenetre = Fenetre()
    fenetre.mainloop()
    
