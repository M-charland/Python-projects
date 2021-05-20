from tkinter import Tk, messagebox
from pymafia_gui import FramePrincipal
from pymafia import Partie
from random import randint


class FenetrePymafia(Tk):
    """
    Classe principale du module pour l'interface du jeu pymafia
    """
    def __init__(self):
        """
        Constructeur de la classe FenetrePymafia
        """
        super().__init__()

        self.title("Pymafia")
        self.LARGEUR, self.HAUTEUR = 1300, 900
        self.geometry("{}x{}".format(self.LARGEUR, self.HAUTEUR))
        self.resizable(0, 0)

        self.partie = None
        self.nombre_joueurs = 2
        self.sens = 1
        self.frames_joueurs = []

        self.gui = FramePrincipal(self)
        self.gui.grid(row=0, column=0)
        self.gui.afficher_frame_menu_principal()

    def creer_partie(self):
        """
        Cree la partie selon nombre_joueurs et ronde_max et assigne un premier joueur
        :return: None
        """
        # Creer objet Partie
        self.nombre_joueurs = self.gui.frame_configuration1.nombre_joueurs.get()
        self.partie = Partie(self.nombre_joueurs, self.nombre_joueurs)
        self.partie.ronde_max = self.gui.frame_configuration1.nombre_rondes.get()
        self.trouver_premier_joueur()
        self.gui.afficher_frame_configuration2()

    def preparer_partie(self):
        """
        Assigne un sens a la partie et debute la partie
        :return: None
        """
        self.partie.sens = self.sens
        self.debuter_partie()

    def debuter_partie(self):
        """
        Affiche les frames du jeu et debute la premiere ronde
        :return: None
        """
        # Configurer GUI selon partie
        self.afficher_jeu()
        self.frames_joueurs = self.gui.frame_jeu.placer_joueurs()
        self.gui.configurer_style_boutons()
        self.gui.configurer_style_labels()

        # Preparer debut partie
        self.partie.preparer_debut_ronde()
        self.trouver_frame_joueur_courant().activer_bouton()
        self.mettre_a_jour_label_jeu()

    def afficher_configurations(self):
        """
        Affiche le frame configuration #1, la tete et le pied de la fenetre
        :return: None
        """
        self.gui.fermer_frame_menu_principal()
        self.gui.afficher_frame_tete()
        self.gui.afficher_frame_pied()
        self.gui.afficher_frame_configuration1()

    def afficher_jeu(self):
        """
        Affiche les frames frame_tete_jeu, frame_jeu et frame_message
        :return: None
        """
        self.gui.fermer_frame_configuration1()
        self.gui.fermer_frame_configuration2()
        self.gui.fermer_frame_instruction()
        self.gui.afficher_frame_tete_jeu()
        self.gui.afficher_frame_jeu()
        self.gui.afficher_frame_message()

    def quitter(self):
        """
        Affiche une fenetre pour fermer la fenetre
        :return: None
        """
        if messagebox.askokcancel("Quitter", "Voulez-vous vraiment quitter Pymafia?"):
            self.destroy()

    def retourner_menu_principal(self):
        """
        Affiche une fenetre pour retourner au menu principal
        :return: None
        """
        message = "Voulez-vous vraiment retourner au menu principal?\n\nSi une partie est en cours, elle sera perdue"
        if messagebox.askokcancel("Retour au menu principal", message, icon="warning"):
            self.gui.afficher_frame_menu_principal()
            self.gui.fermer_frame_menu()

    def recommencer_une_partie(self):
        """
        Affiche une fenetre pour recommencer un partie a partir de configuration #1
        :return: None
        """
        message = "Voulez-vous vraiment créer une nouvelle partie?\n\nSi une partie est en cours, elle sera perdue"
        if messagebox.askokcancel("Nouvelle partie", message, icon="warning"):
            self.afficher_configurations()
            self.gui.fermer_frame_menu()

    def jouer_un_tour(self):
        """
        Joue le tour du joueur courant
        :return: None
        """
        self.trouver_frame_joueur_courant().inactiver_bouton()

        if self.partie.gagnant_ronde is None:
            self.partie.jouer_un_tour()

        else:
            self.partie.terminer_ronde()

        self.trouver_frame_joueur_courant().activer_bouton()
        self.mettre_a_jour_label_jeu()

    def mettre_a_jour_label_score(self):
        """
        Met a jour le texte du label label_score pour tout les joueurs du jeu
        :return: None
        """
        for frame_joueur in self.frames_joueurs:
            frame_joueur.mettre_a_jour_label_score()

    def mettre_a_jour_label_dés(self):
        """
        Met a jour le texte du label label_dés_joueur_X pour tout les joueurs du jeu
        :return: None
        """
        for frame_joueur in self.frames_joueurs:
            frame_joueur.mettre_a_jour_label_dés()

    def mettre_a_jour_label_information_partie(self):
        """
        Met a jour les textes des labels de ronde, message et tour du joueur
        :return: None
        """
        self.gui.frame_message.mettre_a_jour_labels_messages()
        self.gui.frame_tete_jeu.mettre_a_jour_label_ronde()
        self.gui.frame_tete_jeu.mettre_a_jour_label_tour_joueur()

    def mettre_a_jour_label_jeu(self):
        """
        Met a jour les textes des labels de informations de la partie, du score et des dés
        :return: None
        """
        self.mettre_a_jour_label_information_partie()
        self.mettre_a_jour_label_score()
        self.mettre_a_jour_label_dés()

    def trouver_frame_joueur_courant(self):
        """
        Trouve le frame associé au joueur courant
        :return: frame du joueur courant
        """
        for frame_joueur in self.frames_joueurs:
            if frame_joueur.joueur == self.partie.joueur_courant:
                return frame_joueur

    def trouver_premier_joueur(self):
        """
        Trouve le premiere joueur au hasard
        :return: None
        """
        self.partie.premier_joueur = self.partie.joueurs[randint(0, len(self.partie.joueurs) - 1)]
        self.gui.frame_configuration2.identifiant_premier_joueur.set(str(self.partie.premier_joueur.identifiant))
        self.gui.frame_configuration2.mettre_a_jour_messages()


if __name__ == "__main__":
    pymafia = FenetrePymafia()
    pymafia.mainloop()
