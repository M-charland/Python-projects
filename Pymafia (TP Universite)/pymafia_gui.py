"""
Module contenant la description d'une classe pour la fenêtre du jeu Pymafia et de classes secondaires.
"""
from tkinter import Frame, Button, Label, StringVar, Spinbox, IntVar
from random import randrange


class FrameJoueur(Frame):
    """
    Classe pour les frames de tous les joueurs qui prévoit les widgets communs.
    """
    def __init__(self, parent, joueur=None):
        """
        Constructeur de la classe FrameJoueur
        :param parent: reference a la classe FrameJeu
        :param joueur: joueur assigne au frame
        """
        super().__init__(parent)

        self["width"], self["height"] = self.master.master.largeur_frame_joueur, self.master.master.hauteur_frame_joueur

        self.pady_boutons = 0.2 * self.master.master.hauteur_frame_joueur
        self.padx_boutons = 0.14 * self.master.master.largeur_frame_joueur
        self.compte_animation = 0
        self.score = StringVar()

        if joueur is not None:
            self.nom_joueur = StringVar()
            self.joueur = joueur
            self.bouton_rouler_dés = Button(self, textvariable=self.nom_joueur, state="disable",
                                            command=self.animation_rouler_dés)

            self.master.master.boutons_petits.append(self.bouton_rouler_dés)

    def animation_rouler_dés(self):
        """
        Animation des dés
        """
        if self.compte_animation < 5:
            if len(self.joueur.dés) <= 5:
                self.dés_joueur1.set(FramePrincipal.animation_dés(len(self.joueur.dés), vertical=self.vertical))
                self.dés_joueur2.set("")
            else:
                self.dés_joueur1.set(FramePrincipal.animation_dés(5, vertical=self.vertical))
                self.dés_joueur2.set(FramePrincipal.animation_dés(len(self.joueur.dés) - 5, vertical=self.vertical))

            self.compte_animation += 1
            self.after(50, self.animation_rouler_dés)
        else:
            self.master.main.jouer_un_tour()
            self.compte_animation = 0

    def mettre_a_jour_label_score(self):
        """
        Met a jour le texte de label_score
        :return: None
        """
        self.score.set("Score: {}".format(self.joueur.score))

    def mettre_a_jour_label_dés(self):
        # Méthode à être redéfinie dans les classes filles
        pass

    def activer_bouton(self):
        """
        Rend actif le bouton du joueur
        :return: None
        """
        if not self.master.main.partie.partie_terminé:
            self.bouton_rouler_dés['state'] = "normal"

    def inactiver_bouton(self):
        """
        Rend inactif le bouton du joueur
        :return: None
        """
        self.bouton_rouler_dés['state'] = "disable"


class FrameJoueurGauche(FrameJoueur):
    """
    Classe pour un joueur situé à gauche du plateau de jeu
    """
    def __init__(self, parent, joueur=None):
        """
        Constructeur de la classe FrameJoueurGauche
        :param parent: reference a la classe FrameJeu
        :param joueur: joueur assigne au frame
        """
        super().__init__(parent, joueur)

        self.vertical = True

        if joueur is not None:
            self.dés_joueur1 = StringVar()
            self.dés_joueur2 = StringVar()

            self.dés_joueur1.set(str(self.joueur).replace(" ", "\n"))
            self.nom_joueur.set("Joueur {}".format(self.joueur.identifiant))

            self.label_dés_joueur1 = Label(self, textvariable=self.dés_joueur1, height=5, width=1)
            self.label_dés_joueur1.grid(row=0, column=1, rowspan=3, padx=10)

            self.label_dés_joueur2 = Label(self, textvariable=self.dés_joueur2, height=5, width=1)
            self.label_dés_joueur2.grid(row=0, column=2, rowspan=3)

            self.bouton_rouler_dés.grid(row=1, column=0, padx=self.padx_boutons, sticky="n")

            self.label_score = Label(self, textvariable=self.score)
            self.label_score.grid(row=0, column=0, sticky="s")

            self.master.master.labels_moyens.append(self.label_score)
            self.master.master.labels_tres_grands.append(self.label_dés_joueur1)
            self.master.master.labels_tres_grands.append(self.label_dés_joueur2)

    def mettre_a_jour_label_dés(self):
        """
        Met a jour les labels label_dés_joueur1 et label_dés_joueur2 du joueur
        :return: None
        """
        if len(self.joueur.dés) <= 5:
            self.dés_joueur1.set(str(self.joueur).replace(" ", "\n"))
            self.dés_joueur2.set("")
        else:
            self.dés_joueur1.set(str(self.joueur)[0:9].replace(" ", "\n"))
            self.dés_joueur2.set(str(self.joueur)[10:].replace(" ", "\n"))


class FrameJoueurDroite(FrameJoueur):
    """
    Classe pour un joueur situé à droite du plateau de jeu
    """
    def __init__(self, parent, joueur=None):
        """
        Constructeur de la classe FrameJoueurDroite
        :param parent: reference a la classe FrameJeu
        :param joueur: joueur assigne au frame
        """
        super().__init__(parent, joueur)

        self.vertical = True

        if joueur is not None:
            self.dés_joueur1 = StringVar()
            self.dés_joueur2 = StringVar()

            self.dés_joueur1.set(str(self.joueur).replace(" ", "\n"))

            self.nom_joueur.set("Joueur {}".format(self.joueur.identifiant))

            self.label_dés_joueur1 = Label(self, textvariable=self.dés_joueur1, height=5, width=1)
            self.label_dés_joueur1.grid(row=0, column=1, rowspan=3, padx=10)

            self.label_dés_joueur2 = Label(self, textvariable=self.dés_joueur2, height=5, width=1)
            self.label_dés_joueur2.grid(row=0, column=0, rowspan=3)

            self.bouton_rouler_dés.grid(row=1, column=2, padx=self.padx_boutons, sticky="n")

            self.label_score = Label(self, textvariable=self.score)
            self.label_score.grid(row=0, column=2, sticky="s")

            self.master.master.labels_moyens.append(self.label_score)
            self.master.master.labels_tres_grands.append(self.label_dés_joueur1)
            self.master.master.labels_tres_grands.append(self.label_dés_joueur2)

    def mettre_a_jour_label_dés(self):
        """
        Met a jour les labels label_dés_joueur1 et label_dés_joueur2 du joueur
        :return: None
        """
        if len(self.joueur.dés) <= 5:
            self.dés_joueur1.set(str(self.joueur).replace(" ", "\n"))
            self.dés_joueur2.set("")
        else:
            self.dés_joueur1.set(str(self.joueur)[0:9].replace(" ", "\n"))
            self.dés_joueur2.set(str(self.joueur)[10:].replace(" ", "\n"))


class FrameJoueurHaut(FrameJoueur):
    """
    Classe pour un joueur situé en haut du plateau de jeu
    """
    def __init__(self, parent, joueur=None):
        """
        Constructeur de la classe FrameJoueurHaut
        :param parent: reference a la classe FrameJeu
        :param joueur: joueur assigne au frame
        """
        super().__init__(parent, joueur)

        self.vertical = False

        if joueur is not None:
            self.dés_joueur1 = StringVar()
            self.dés_joueur2 = StringVar()

            self.dés_joueur1.set(str(self.joueur))

            self.nom_joueur.set("Joueur {}".format(self.joueur.identifiant))

            self.label_dés_joueur1 = Label(self, textvariable=self.dés_joueur1, width=10)
            self.label_dés_joueur1.grid(row=2, column=0)

            self.label_dés_joueur2 = Label(self, textvariable=self.dés_joueur2, width=10)
            self.label_dés_joueur2.grid(row=3, column=0)

            self.bouton_rouler_dés.grid(row=1, column=0, pady=(0, self.pady_boutons), sticky="n")

            self.label_score = Label(self, textvariable=self.score)
            self.label_score.grid(row=0, column=0, sticky="s")

            self.master.master.labels_moyens.append(self.label_score)
            self.master.master.labels_tres_grands.append(self.label_dés_joueur1)
            self.master.master.labels_tres_grands.append(self.label_dés_joueur2)

    def mettre_a_jour_label_dés(self):
        """
        Met a jour les labels label_dés_joueur1 et label_dés_joueur2 du joueur
        :return: None
        """
        if len(self.joueur.dés) <= 5:
            self.dés_joueur1.set(str(self.joueur))
            self.dés_joueur2.set("")
        else:
            self.dés_joueur1.set(str(self.joueur)[0:9])
            self.dés_joueur2.set(str(self.joueur)[10:])


class FrameJoueurBas(FrameJoueur):
    """
    Classe pour un joueur situé en bas du plateau de jeu
    """
    def __init__(self, parent, joueur=None):
        """
        Constructeur de la classe FrameJoueurBas
        :param parent: reference a la classe FrameJeu
        :param joueur: joueur assigne au frame
        """
        super().__init__(parent, joueur)

        self.vertical = False

        if joueur is not None:
            self.dés_joueur1 = StringVar()
            self.dés_joueur2 = StringVar()

            self.dés_joueur1.set(str(self.joueur))

            self.nom_joueur.set("Joueur {}".format(self.joueur.identifiant))

            self.label_dés_joueur1 = Label(self, textvariable=self.dés_joueur1, width=10)
            self.label_dés_joueur1.grid(row=1, column=0)

            self.label_dés_joueur2 = Label(self, textvariable=self.dés_joueur2, width=10)
            self.label_dés_joueur2.grid(row=0, column=0)

            self.bouton_rouler_dés.grid(row=2, column=0, pady=(self.pady_boutons, 0), sticky="s")

            self.label_score = Label(self, textvariable=self.score)
            self.label_score.grid(row=3, column=0, sticky="n")

            self.master.master.labels_moyens.append(self.label_score)
            self.master.master.labels_tres_grands.append(self.label_dés_joueur1)
            self.master.master.labels_tres_grands.append(self.label_dés_joueur2)

    def mettre_a_jour_label_dés(self):
        """
        Met a jour les labels label_dés_joueur1 et label_dés_joueur2 du joueur
        :return: None
        """
        if len(self.joueur.dés) <= 5:
            self.dés_joueur1.set(str(self.joueur))
            self.dés_joueur2.set("")
        else:
            self.dés_joueur1.set(str(self.joueur)[0:9])
            self.dés_joueur2.set(str(self.joueur)[10:])


class FrameMenuPrincipal(Frame):
    """
    Classe pour le menu principal
    """
    def __init__(self, parent):
        """
        Constructeur de la classe FrameMenuPrincipal
        :param parent: reference a la classe FramePrincipal
        """
        super().__init__(parent)

        self["width"], self["height"] = parent.largeur_frame_menu_principal, parent.hauteur_frame_menu_principal
        self["borderwidth"], self["relief"] = 2, "raised"


        self.baniere_dés_verticale = StringVar()
        self.baniere_dés_horizontale = StringVar()

        self.label_baniere_dés_haut = Label(self, textvariable=self.baniere_dés_horizontale)
        self.label_baniere_dés_haut.grid(row=0, column=1, sticky="n")

        self.label_baniere_dés_bas = Label(self, textvariable=self.baniere_dés_horizontale)
        self.label_baniere_dés_bas.grid(row=4, column=1, sticky="s")

        self.label_baniere_dés_gauche = Label(self, textvariable=self.baniere_dés_verticale)
        self.label_baniere_dés_gauche.grid(row=0, column=0, rowspan=5, sticky="w", padx=7)

        self.label_baniere_dés_droite = Label(self, textvariable=self.baniere_dés_verticale)
        self.label_baniere_dés_droite.grid(row=0, column=2, rowspan=5, sticky="e", padx=7)

        self.label_bienvenue = Label(self, text="Bienvenue sur Pymafia!")
        self.label_bienvenue.grid(row=1, column=1, sticky="s")

        self.bouton_nouvelle_partie = Button(self, text="Nouvelle partie",
                                             command=self.master.master.afficher_configurations)
        self.bouton_nouvelle_partie.grid(row=2, column=1, sticky="s")

        self.bouton_quitter = Button(self, text="Quitter", command=self.master.master.quitter)
        self.bouton_quitter.grid(row=3, column=1)

        parent.labels_tres_grands.append(self.label_baniere_dés_haut)
        parent.labels_tres_grands.append(self.label_baniere_dés_bas)
        parent.labels_tres_grands.append(self.label_baniere_dés_droite)
        parent.labels_tres_grands.append(self.label_baniere_dés_gauche)
        parent.labels_titre.append(self.label_bienvenue)
        parent.boutons_grands.append(self.bouton_nouvelle_partie)
        parent.boutons_grands.append(self.bouton_quitter)

        self.after(250, self.tourner_dés_baniere)

    def tourner_dés_baniere(self):
        """
        Animer les dés du contour de la fenetre de menu principal
        :return: None
        """
        self.baniere_dés_horizontale.set(FramePrincipal.animation_dés(28))
        self.baniere_dés_verticale.set(FramePrincipal.animation_dés(17, vertical=True))
        self.after(250, self.tourner_dés_baniere)


class FrameConfiguration1(Frame):
    """
    Classe pour la premiere fenetre de configuration (nombres de joueurs et nombre de rondes)
    """
    def __init__(self, parent):
        """
        Constructeur de la classe FrameConfiguration1
        :param parent: reference a la classe FramePrincipal
        """
        super().__init__(parent)

        self["width"], self["height"] = parent.largeur_frame_configuration, parent.hauteur_frame_configuration
        self["borderwidth"], self["relief"] = 2, "raised"

        self.nombre_joueurs = IntVar(value=2)
        self.nombre_rondes = IntVar(value=1)

        self.label_nombre_joueurs = Label(self, text="Nombre de joueurs")
        self.label_nombre_joueurs.grid(row=0, column=0, sticky="s", pady=15)

        self.spinbox_nombre_joueurs = Spinbox(self, from_=2, to=4, justify="center",
                                              command=self.mettre_a_jour_nombre_joueurs)
        self.spinbox_nombre_joueurs.grid(row=1, column=0, sticky="n", pady=15)

        self.label_nombre_rondes = Label(self, text="Nombre de rondes")
        self.label_nombre_rondes.grid(row=2, column=0, sticky="s", pady=15)

        self.spinbox_nombre_rondes = Spinbox(self, from_=1, to=10, justify="center",
                                             command=self.mettre_a_jour_nombre_rondes)
        self.spinbox_nombre_rondes.grid(row=3, column=0, sticky="n", pady=15)

        self.bouton_suivant = Button(self, text="Suivant", command=self.master.master.creer_partie)
        self.bouton_suivant.grid(row=4, column=0, sticky="n", pady=15)

        parent.labels_grands.append(self.label_nombre_joueurs)
        parent.labels_grands.append(self.spinbox_nombre_joueurs)
        parent.labels_grands.append(self.label_nombre_rondes)
        parent.labels_grands.append(self.spinbox_nombre_rondes)
        parent.boutons_grands.append(self.bouton_suivant)

    def mettre_a_jour_nombre_joueurs(self):
        """
        Met a jour la variable nombre_joueurs selon spinbox_nombre_joueurs
        :return: None
        """
        self.nombre_joueurs.set(int(self.spinbox_nombre_joueurs.get()))

    def mettre_a_jour_nombre_rondes(self):
        """
        Met a jour la variable nombre_rondes selon spinbox_nombre_tours
        :return: None
        """
        self.nombre_rondes.set(int(self.spinbox_nombre_rondes.get()))


class FrameConfiguration2(Frame):
    """
    Classe pour la deuxieme fenetre de configuration (premier joueur et sens)
    """
    def __init__(self, parent):
        """
        Constructeur de la classe FrameConfiguration2
        :param parent: reference a la classe FramePrincipal
        """
        super().__init__(parent)

        self["width"], self["height"] = parent.largeur_frame_configuration, parent.hauteur_frame_configuration
        self["borderwidth"], self["relief"] = 2, "raised"

        self.identifiant_premier_joueur = StringVar()
        self.message_premier_joueur = StringVar()
        self.message_choix_sens = StringVar()

        self.label_hasard = Label(self, text="Le premier joueur a été déterminé par hasard\n")
        self.label_hasard.grid(row=0, column=0, columnspan=2, sticky="s")

        self.label_premier_joueur = Label(self, textvariable=self.message_premier_joueur)
        self.label_premier_joueur.grid(row=1, column=0, columnspan=2, sticky="n")

        self.label_choix_sens = Label(self, textvariable=self.message_choix_sens)
        self.label_choix_sens.grid(row=2, column=0, columnspan=2)

        self.bouton_croissant = Button(self, text="Croissant", command=self.master.master.preparer_partie)
        self.bouton_croissant.grid(row=3, column=0, sticky="ne", padx=10)

        self.bouton_decroissant = Button(self, text="Décroissant", command=self.creer_partie_sens_decroissant)
        self.bouton_decroissant.grid(row=3, column=1, sticky="nw", padx=10)

        parent.labels_grands.append(self.label_hasard)
        parent.labels_grands.append(self.label_premier_joueur)
        parent.labels_grands.append(self.label_choix_sens)
        parent.boutons_grands.append(self.bouton_croissant)
        parent.boutons_grands.append(self.bouton_decroissant)

    def creer_partie_sens_decroissant(self):
        """
        Change la valeur du sens de la partie a -1 et creer un objet Partie
        :return: None
        """
        self.master.sens = -1
        self.master.master.preparer_partie()

    def mettre_a_jour_messages(self):
        """
        Met a jour le texte des labels label_hasard et label_premier_joueur
        """
        self.message_premier_joueur.set("Le joueur {} est le premier joueur!"
                                        .format(self.identifiant_premier_joueur.get()))

        self.message_choix_sens.set("Le joueur {} choisit donc le sens de la partie"
                                    .format(self.identifiant_premier_joueur.get()))


class FrameInstruction(Frame):
    """
    Classe pour les instructions du jeu
    """
    def __init__(self, parent):
        """
        Constructeur de la classe FrameInstruction
        :param parent: reference a la classe FramePrincipal
        :return: None
        """
        super().__init__(parent)

        self["width"], self["height"] = parent.largeur_frame_instruction, parent.hauteur_frame_instruction
        self["borderwidth"], self["relief"] = 2, "raised"

        self.texte = "Vous pouvez jouer entre 2 et 8 joueurs, mais le jeu est plus enlevant entre 3 et 5 joueurs.\n" \
                     "Au départ, chaque joueur dispose de 5 dés traditionnels à 6 faces et 100 points.\n" \
                     "\nAvant le début de la première ronde, chaque joueur joue deux dés. " \
                     "Le joueur ayant le plus haut résultat commencera.\n" \
                     "Tant qu’il y a égalité au plus haut score entre plusieurs joueurs, ces derniers relancent les " \
                     "dés. \nAutour d’une table, le jeu peut se jouer autant dans le sens horaire qu’anti-horaire.\n" \
                     "C’est le premier joueur qui décide\n" \
                     "\nLorsque c’est son tour, un joueur roule tous ses dés. Les dés ayant la valeur 6 sont passés \n"\
                     "au prochain joueur. Les dés de valeur 1 sont retirés du jeu.\n" \
                     "\nLe jeu continue jusqu’à ce qu’un joueur n’ait plus aucun dé. Ceci termine la ronde.\n" \
                     "Les autres joueurs roulent alors leurs dés restants et comptent le total des dés.\n" \
                     "Ils perdent alors le nombre de points obtenus sur les dés et donnent ces points au gagnant \n" \
                     "de la ronde.\n\nSi un joueur vient à ne plus avoir de point, il se retire du jeu.\n" \
                     "Dans ce cas, il donne le nombre de points qu’il lui restait plutôt que la somme des dés joués.\n"\
                     "\nLorsqu’on recommence une ronde, tous les joueurs retrouvent 5 dés.\n" \
                     "Le gagnant de la ronde précédente est celui qui commence la nouvelle ronde."

        self.label_instructions_titre = Label(self, text="Les règles du jeu sont les suivantes :")
        self.label_instructions_titre.grid(row=0, column=0, sticky="s")

        self.label_instructions = Label(self, text=self.texte)
        self.label_instructions.grid(row=1, column=0)

        self.bouton_compris = Button(self, text="J'ai compris!", command=parent.fermer_frame_instruction)
        self.bouton_compris.grid(row=2, column=0)

        parent.labels_grands.append(self.label_instructions_titre)
        parent.labels_moyens.append(self.label_instructions)
        parent.boutons_moyens.append(self.bouton_compris)


class FrameMessage(Frame):
    """
    Classe pour les frames messages avec des widgets communs.
    """
    def __init__(self, parent):
        """
        Constructeur de la classe FrameMessage
        :param parent: reference a la classe FramePrincipal
        """
        super().__init__(parent)

        self["width"], self["height"] = parent.largeur_frame_message, parent.hauteur_frame_message
        self["borderwidth"], self["relief"] = 1, "sunken"

        self.message = StringVar()

        self.label_message = Label(self, textvariable=self.message)
        self.label_message.grid(row=0, column=0)

        parent.labels_petits.append(self.label_message)

    def mettre_a_jour_labels_messages(self):
        """
        Met a jour le texte du label label_message
        :return: None
        """
        self.message.set(self.master.master.partie.message_narration)


class FrameTeteJeu(Frame):
    """
    Classe pour la tete du cadre du jeu (information tour du joueur et rondes)
    """
    def __init__(self, parent):
        """
        Constructeur de la classe FrameTeteJeu
        :param parent: reference a la classe FramePrincipal
        """
        super().__init__(parent)

        self["width"], self["height"] = parent.largeur_frame_tete_jeu, parent.hauteur_frame_tete_jeu
        self["borderwidth"], self["relief"] = 1, "sunken"
        self.ronde = StringVar()
        self.tour_joueur = StringVar()

        self.label_tour_joueur = Label(self, textvariable=self.tour_joueur, height=1)
        self.label_tour_joueur.grid(row=0, column=0)

        self.label_ronde = Label(self, textvariable=self.ronde, height=1)
        self.label_ronde.grid(row=0, column=0, sticky="w", padx=15)

        parent.labels_moyens.append(self.label_tour_joueur)
        parent.labels_moyens.append(self.label_ronde)

    def mettre_a_jour_label_ronde(self):
        """
        Met a jour le texte du label label_ronde
        :return: None
        """
        self.ronde.set("Ronde : {} / {}".format(self.master.master.partie.ronde, self.master.master.partie.ronde_max))

    def mettre_a_jour_label_tour_joueur(self):
        """
        Met a jour le texte du label label_tour_joueur
        :return: None
        """
        self.tour_joueur.set(self.master.master.partie.message_tete_jeu)


class FrameJeu(Frame):
    """
    Classe pour le cadre du jeu (joueurs et leurs dés)
    """
    def __init__(self, parent):
        """
        Constructeur de la classe FrameJeu
        :param parent: reference a la classe FramePrincipal
        """
        super().__init__(parent)

        self["width"], self["height"] = parent.largeur_frame_jeu, parent.hauteur_frame_jeu

        self.main = self.master.master
        self.frame_joueur_haut = None
        self.frame_joueur_droite = None
        self.frame_joueur_bas = None
        self.frame_joueur_gauche = None
        self.frame_joueurs = []

    def placer_joueurs(self):
        """
        Creer les objet Joueur selon nombre_joueurs et leur assigne un frame
        :return: (list) liste des joueurs
        """
        # Enlever joueurs des parties precedentes
        if self.frame_joueurs:
            for frame in self.frame_joueurs:
                frame.grid_remove()

        # Creer frames vides a gauche et a droite pour egaliser l'espacement des frames
        frame_gauche = FrameJoueur(self)
        frame_gauche.grid(row=1, column=2)

        frame_gauche = FrameJoueur(self)
        frame_gauche.grid(row=1, column=0)

        # Placer joueur 1
        joueurs_actifs = self.master.master.partie.joueurs_actifs
        self.frame_joueur_haut = FrameJoueurHaut(self, joueurs_actifs[0])
        self.frame_joueur_haut.grid(row=0, column=1)
        self.frame_joueurs.append(self.frame_joueur_haut)

        # Placement pour partie a 2
        if len(joueurs_actifs) == 2:
            self.frame_joueur_bas = FrameJoueurBas(self, joueurs_actifs[1])
            self.frame_joueur_bas.grid(row=2, column=1)

            self.frame_joueurs.append(self.frame_joueur_bas)

        # Placement pour partie a 3
        elif len(joueurs_actifs) > 2:
            self.frame_joueur_droite = FrameJoueurDroite(self, joueurs_actifs[1])
            self.frame_joueur_droite.grid(row=1, column=2)

            self.frame_joueur_bas = FrameJoueurBas(self, joueurs_actifs[2])
            self.frame_joueur_bas.grid(row=2, column=1)

            self.frame_joueurs.append(self.frame_joueur_droite)
            self.frame_joueurs.append(self.frame_joueur_bas)

            # Placement pour partie a 4
            if len(joueurs_actifs) == 4:
                self.frame_joueur_gauche = FrameJoueurGauche(self, joueurs_actifs[3])
                self.frame_joueur_gauche.grid(row=1, column=0)

                self.frame_joueurs.append(self.frame_joueur_gauche)

        # Configurer positionnements interieur des frames
        for frame in self.frame_joueurs:
            FramePrincipal.configurer_positionnement_interieur_frame(frame)

        FramePrincipal.configurer_positionnement_interieur_frame(self, True)

        return self.frame_joueurs


class FrameTetePied(Frame):
    """
    Classe pour les widgets communs de FrameTete et FramePied
    """
    def __init__(self, parent):
        """
        Constructeur de la classe FrameTetePied
        :param parent: reference a la classe FramePrincipal
        """
        super().__init__(parent)

        self["width"], self["height"] = parent.largeur_frame_tete_et_pied, parent.hauteur_frame_tete_et_pied
        self["borderwidth"], self["relief"] = 2, "raised"

        self.baniere_gauche = ""
        self.baniere_droite = ""

        for i in range(6):
            self.baniere_gauche += str(chr(9856 + i)) + " "
            self.baniere_droite += " " + str(chr(9861 - i))

        self.label_baniere_gauche = Label(self, text=self.baniere_gauche, padx=15)
        self.label_baniere_gauche.grid(row=0, column=0, sticky="w")

        self.label_baniere_droite = Label(self, text=self.baniere_droite, padx=15)
        self.label_baniere_droite.grid(row=0, column=2, sticky="e")

        parent.labels_tres_grands.append(self.label_baniere_gauche)
        parent.labels_tres_grands.append(self.label_baniere_droite)


class FrameTete(FrameTetePied):
    """
    Classe pour l'entete du jeu
    """
    def __init__(self, parent):
        """
        Constructeur de la classe FrameTete
        :param parent: reference a la classe FramePrincipal
        """
        super().__init__(parent)

        self.texte_entete = StringVar()
        self.nom_page_actuelle = StringVar()

        self.label_entete = Label(self, textvariable=self.texte_entete)
        self.label_entete.grid(row=0, column=1)

        parent.labels_grands.append(self.label_entete)

    def mettre_a_jour_label_entete(self):
        """
        Met a jour le texte du label label_entete
        :return: None
        """
        texte_entete = self.nom_page_actuelle.get()
        self.texte_entete.set(texte_entete)


class FramePied(FrameTetePied):
    """
    Classe pour le pied de la fenetre
    """
    def __init__(self, parent):
        """
        Constructeur de la classe FramePied
        :param parent: reference a la classe FramePrincipal
        """
        super().__init__(parent)

        self.bouton_menu = Button(self, text="Menu", command=parent.afficher_frame_menu)
        self.bouton_menu.grid(row=0, column=1)

        parent.boutons_moyens.append(self.bouton_menu)


class FrameMenu(Frame):
    """
    Classe pour le menu de boutons
    """
    def __init__(self, parent):
        """
        Constructeur de la classe FrameMenu
        :param parent: reference a la classe FramePrincipal
        """
        super().__init__(parent)

        self["width"], self["height"] = parent.largeur_frame_menu, parent.hauteur_frame_menu
        self["borderwidth"], self["relief"] = 2, "raised"
        self.bouton_retour = StringVar()

        self.bouton_retour_jeu = Button(self, text="Retourner à la partie", command=self.presser_bouton_retour_au_jeu)
        self.bouton_retour_jeu.grid(row=0, column=0)

        self.bouton_nouvelle_partie = Button(self, text="Nouvelle partie",
                                             command=self.master.master.recommencer_une_partie)
        self.bouton_nouvelle_partie.grid(row=1, column=0)

        self.bouton_instructions = Button(self, text="Instructions", command=self.presser_bouton_instructions)
        self.bouton_instructions.grid(row=2, column=0)

        self.bouton_menu_principal = Button(self, text="Menu principal",
                                            command=self.master.master.retourner_menu_principal)
        self.bouton_menu_principal.grid(row=3, column=0)

        self.bouton_quitter = Button(self, text="Quitter", command=self.master.master.quitter)
        self.bouton_quitter.grid(row=4, column=0)

        parent.boutons_grands.append(self.bouton_retour_jeu)
        parent.boutons_grands.append(self.bouton_nouvelle_partie)
        parent.boutons_grands.append(self.bouton_instructions)
        parent.boutons_grands.append(self.bouton_menu_principal)
        parent.boutons_grands.append(self.bouton_quitter)

    def presser_bouton_retour_au_jeu(self):
        """
        Met en avant plan le frame jeu et ferme le menu
        :return: None
        """
        self.master.afficher_jeu()
        self.master.fermer_frame_menu()

    def presser_bouton_instructions(self):
        """
        Met en avant plan le frame instructions et ferme le menu
        :return: None
        """
        self.master.afficher_frame_instruction()
        self.master.fermer_frame_menu()


class FramePrincipal(Frame):
    """
    Classe pour l'ensemble du jeu, parent des autres classes frame
    """

    def __init__(self, parent):
        """
        Constructeur de la classe FramePrincipal
        :param parent: reference a la classe FramePrincipal
        """
        super().__init__(parent)

        # Listes pour modifications styles
        self.boutons_grands = []
        self.boutons_moyens = []
        self.boutons_petits = []
        self.labels_titre = []
        self.labels_tres_grands = []
        self.labels_grands = []
        self.labels_moyens = []
        self.labels_petits = []

        # Dimensions frames selon dimensions fenetre
        self["width"], self["height"] = parent.LARGEUR, parent.HAUTEUR

        self.largeur_frame_menu_principal = parent.LARGEUR
        self.hauteur_frame_menu_principal = parent.HAUTEUR

        self.largeur_frame_tete_et_pied = parent.LARGEUR
        self.hauteur_frame_tete_et_pied = int(0.075 * parent.HAUTEUR)

        self.largeur_frame_jeu = int(0.65 * parent.LARGEUR)
        self.hauteur_frame_jeu = int(0.81 * parent.HAUTEUR)

        self.largeur_frame_tete_jeu = parent.LARGEUR
        self.hauteur_frame_tete_jeu = parent.HAUTEUR - self.hauteur_frame_jeu - 2 * self.hauteur_frame_tete_et_pied

        self.largeur_frame_joueur = int(0.33 * self.largeur_frame_jeu)
        self.hauteur_frame_joueur = int(0.33 * self.hauteur_frame_jeu)

        self.largeur_frame_message = parent.LARGEUR - self.largeur_frame_jeu
        self.hauteur_frame_message = self.hauteur_frame_jeu

        self.largeur_frame_configuration = parent.LARGEUR
        self.hauteur_frame_configuration = self.hauteur_frame_jeu + self.hauteur_frame_tete_jeu

        self.largeur_frame_instruction = parent.LARGEUR
        self.hauteur_frame_instruction = self.hauteur_frame_configuration

        self.largeur_frame_menu = self.largeur_frame_instruction
        self.hauteur_frame_menu = self.hauteur_frame_configuration

        # Creation des frames
        self.frame_menu_principal = FrameMenuPrincipal(self)
        self.frame_instruction = FrameInstruction(self)
        self.frame_configuration1 = FrameConfiguration1(self)
        self.frame_configuration2 = FrameConfiguration2(self)
        self.frame_jeu = FrameJeu(self)
        self.frame_tete_jeu = FrameTeteJeu(self)
        self.frame_message = FrameMessage(self)
        self.frame_tete = FrameTete(self)
        self.frame_pied = FramePied(self)
        self.frame_menu = FrameMenu(self)

        # Configuration des frames
        self.configurer_style_boutons()
        self.configurer_style_labels()
        FramePrincipal.configurer_positionnement_interieur_frame(self)
        FramePrincipal.configurer_positionnement_interieur_frame(self.frame_menu_principal)
        FramePrincipal.configurer_positionnement_interieur_frame(self.frame_instruction)
        FramePrincipal.configurer_positionnement_interieur_frame(self.frame_configuration1)
        FramePrincipal.configurer_positionnement_interieur_frame(self.frame_configuration2)
        FramePrincipal.configurer_positionnement_interieur_frame(self.frame_tete_jeu)
        FramePrincipal.configurer_positionnement_interieur_frame(self.frame_message)
        FramePrincipal.configurer_positionnement_interieur_frame(self.frame_tete)
        FramePrincipal.configurer_positionnement_interieur_frame(self.frame_pied)
        FramePrincipal.configurer_positionnement_interieur_frame(self.frame_menu)

    # Methodes pour afficher frames
    def afficher_frame_menu_principal(self):
        """
        Met en avant plan le frame menu principal
        :return: None
        """
        self.frame_menu_principal.grid(row=0, column=0)
        self.frame_menu_principal.tkraise()
        self.frame_menu.bouton_retour_jeu["state"] = "disable"

    def afficher_frame_configuration1(self):
        """
        Met en avant plan le frame configuration #1
        :return: None
        """
        self.frame_configuration1.grid(row=1, column=0, rowspan=2, columnspan=2)
        self.frame_configuration1.tkraise()
        self.frame_tete.nom_page_actuelle.set("Configuration de la partie")
        self.frame_menu.bouton_retour_jeu["state"] = "disable"
        self.frame_tete.mettre_a_jour_label_entete()

    def afficher_frame_configuration2(self):
        """
        Met en avant plan le frame configuration #2
        :return: None
        """
        self.frame_configuration2.grid(row=1, column=0, rowspan=2, columnspan=2)
        self.frame_configuration2.tkraise()

    def afficher_frame_instruction(self):
        """
        Met en avant plan le frame instructions
        :return: None
        """
        self.frame_instruction.grid(row=1, column=0, rowspan=2, columnspan=2)
        self.frame_instruction.tkraise()
        self.frame_tete.nom_page_actuelle.set("Instructions")
        self.fermer_frame_menu()
        self.frame_tete.mettre_a_jour_label_entete()

    def afficher_frame_jeu(self):
        """
        Met en avant plan le frame jeu
        :return: None
        """
        self.frame_jeu.grid(row=2, column=0)
        self.frame_jeu.tkraise()
        self.frame_tete.nom_page_actuelle.set("Partie en cours")
        self.frame_menu.bouton_retour_jeu["state"] = "normal"
        self.frame_tete.mettre_a_jour_label_entete()

    def afficher_frame_tete_jeu(self):
        """
        Met en avant plan le frame tete jeu
        :return: None
        """
        self.frame_tete_jeu.grid(row=1, column=0, columnspan=2)
        self.frame_tete_jeu.tkraise()

    def afficher_frame_message(self):
        """
        Met en avant plan le frame message
        :return: None
        """
        self.frame_message.grid(row=2, column=1)
        self.frame_message.tkraise()

    def afficher_frame_tete(self):
        """
        Met en avant plan le frame tete
        :return: None
        """
        self.frame_tete.grid(row=0, column=0, columnspan=2)
        self.frame_tete.tkraise()

    def afficher_frame_pied(self):
        """
        Met en avant plan le frame pied
        :return: None
        """
        self.frame_pied.grid(row=3, column=0, columnspan=2)
        self.frame_pied.tkraise()

    def afficher_frame_menu(self):
        """
        Met en avant plan le frame menu
        :return: None
        """
        if self.frame_pied.bouton_menu["relief"] == "raised":
            self.frame_menu.grid(row=1, column=0, rowspan=2, columnspan=2)
            self.frame_menu.tkraise()
            self.frame_pied.bouton_menu["relief"] = "sunken"
        else:
            self.fermer_frame_menu()

    # Methodes pour fermer frames
    def fermer_frame_menu_principal(self):
        """
        Ferme le frame menu principal
        :return: None
        """
        self.frame_menu_principal.grid_remove()

    def fermer_frame_configuration1(self):
        """
        Ferme le frame configuration #1
        :return: None
        """
        self.frame_configuration1.grid_remove()

    def fermer_frame_configuration2(self):
        """
        Ferme le frame configuration #2
        :return: None
        """
        self.frame_configuration2.grid_remove()

    def fermer_frame_instruction(self):
        """
        Ferme le frame instructions
        :return: None
        """
        self.frame_instruction.grid_remove()

    def fermer_frame_jeu(self):
        """
        Ferme le frame jeu
        :return: None
        """
        self.frame_jeu.grid_remove()

    def fermer_frame_tete_jeu(self):
        """
        Ferme le frame tete jeu
        :return: None
        """
        self.frame_tete_jeu.grid_remove()

    def fermer_frame_message(self):
        """
        Ferme le frame message
        :return: None
        """
        self.frame_message.grid_remove()

    def fermer_frame_tete(self):
        """
        Ferme le frame tete
        :return: None
        """
        self.frame_tete.grid_remove()

    def fermer_frame_pied(self):
        """
        Ferme le frame pied
        :return: None
        """
        self.frame_pied.grid_remove()

    def fermer_frame_menu(self):
        """
        ferme le frame menu
        :return: None
        """
        self.frame_menu.grid_remove()
        self.frame_pied.bouton_menu["relief"] = "raised"

    # Methode configuration widgets
    def configurer_style_boutons(self):
        """
        Configure la police et la dimension des boutons
        :return: None
        """
        for bouton in self.boutons_petits:
            bouton["width"], bouton["height"] = 10, 4
            bouton["borderwidth"] = 5
            bouton["font"] = ("Courrier", 12)
        for bouton in self.boutons_moyens:
            bouton["width"], bouton["height"] = 15, 1
            bouton["borderwidth"] = 5
            bouton["font"] = ("Courrier", 18)
        for bouton in self.boutons_grands:
            bouton["width"], bouton["height"] = 18, 1
            bouton["borderwidth"] = 10
            bouton["font"] = ("Courrier", 28)

    def configurer_style_labels(self):
        """
        Configure la police des labels
        :return: None
        """
        for label in self.labels_petits:
            label["font"] = ("Courrier", 12)
        for label in self.labels_moyens:
            label["font"] = ("Courrier", 14)
        for label in self.labels_grands:
            label["font"] = ("Courrier", 24)
        for label in self.labels_tres_grands:
            label["font"] = ("Courrier", 32)
        for label in self.labels_titre:
            label["font"] = ("Courrier", 48)

    @staticmethod
    def configurer_positionnement_interieur_frame(cadre, propagate=False):
        """
        Configure le positionnement et la dimension des widget a l'interieur des frames
        :param cadre:
        :param propagate:
        :return: None
        """
        cadre.grid_propagate(propagate)
        nombre_colonnes, nombre_ranges = cadre.grid_size()
        for i in range(nombre_ranges):
            cadre.grid_rowconfigure(i, weight=1)
        for i in range(nombre_colonnes):
            cadre.grid_columnconfigure(i, weight=1)

    @staticmethod
    def animation_dés(nombre_dés, vertical=False):
        """
        Cree une animation de dés en generant des valeurs random
        :param nombre_dés: (int) nombre de dés a animer
        :param vertical: (bool) True: colonne, False: rangée
        :return: (string) animation des dés
        """
        dés_random = [chr(randrange(9856, 9862)) for i in range(nombre_dés)]
        espacement = " "
        if vertical:
            espacement = "\n"

        return espacement.join(str(i) for i in dés_random)
