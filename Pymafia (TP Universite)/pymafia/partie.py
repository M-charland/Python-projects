"""
Module de la classe Partie
"""

from pymafia.joueur_humain import JoueurHumain
from pymafia.joueur_ordinateur import JoueurOrdinateur
from random import shuffle


class Partie:
    """
    Documentation de la classe Partie
    Attributes:
        joueurs (list): Liste des joueurs au départ de la partie
        joueurs_actifs (list): Liste des joueurs qui ont encore des points (score supérieur à 0)
        premier_joueur (Joueur): Premier joueur de la ronde
        joueur_courant (Joueur): Joueur dont c'est le tour
        joueur_suivant (Joueur): Joueur dont ce sera le tour lorsque le joueur_courant aura joué (prochain joueur actif)
        ronde (int): Nombre de la ronde actuelle
        sens (int): Nombre qui indique le sens du tour (1, croissant; -1, décroissant)
    """

    def __init__(self, nombre_joueurs, nombre_joueurs_humains):
        """
        Constructeur de la classe Partie
        Args:
            nombre_joueurs (int): Nombre de joueurs de la partie
            nombre_joueurs_humains (int): Nombre de joueurs humains de la partie
        """
        self.joueurs = self.creer_joueurs(nombre_joueurs, nombre_joueurs_humains)
        self.joueurs_actifs = list(self.joueurs)
        self.premier_joueur = self.joueurs[0]
        self.joueur_courant = self.joueurs[0]
        self.joueur_suivant = self.joueurs[1]
        self.ronde = 1
        self.ronde_max = 10
        self.sens = 1
        self.message_narration = "Début de la partie\n\n\n\nPour consulter les rêgles du jeu," \
                                          " dirigez-vous dans l'onglet\nInstructions du menu"
        self.message_tete_jeu = ""
        self.tours_fin_de_ronde_joué = 1
        self.gagnant_ronde = None
        self.partie_terminé = False

    @staticmethod
    def creer_joueurs(nombre_joueurs, nombre_joueurs_humains):
        """
        Méthode statique qui crée la liste de joueurs de la partie.
        Dans le cas où des joueurs ordinateurs sont permis, les joueurs humains et ordinateurs sont
        mélangés au hasard dans la liste de joueurs.
        Args:
            nombre_joueurs (int): Nombre de joueurs de la partie
            nombre_joueurs_humains (int): Nombre de joueurs humains de la partie

        Returns:
            list: Liste des joueurs
        """
        joueurs = []
        # Ajout des joueurs humains et ordinateurs à la liste
        for i in range(nombre_joueurs_humains):
            joueurs.append(JoueurHumain(0))
        for i in range(nombre_joueurs - nombre_joueurs_humains):
            joueurs.append(JoueurOrdinateur(0))
        # Mélange de la liste des joueurs
        shuffle(joueurs)
        # Modification de l'identifiant des joueurs selon la position dans la liste
        for i, joueur in enumerate(joueurs):
            joueur.identifiant = i + 1
        return joueurs

    def preparer_debut_ronde(self):
        self.gagnant_ronde = None
        self.tours_fin_de_ronde_joué = 1
        self.joueur_courant = self.premier_joueur
        self.determiner_joueur_suivant(self.joueurs_actifs)
        self.reinitialiser_dés_joueurs()
        self.message_tete_jeu = "Début de la ronde {} par le joueur {}" \
            .format(self.ronde, self.joueur_courant.identifiant)

    @staticmethod
    def trouver_joueurs_au_plus_haut_total(liste_joueurs):
        score_joueurs_2_dés = [joueur.calculer_points() for joueur in liste_joueurs]
        indices_du_plus_haut_score = Partie.trouver_indices_max(score_joueurs_2_dés)
        joueurs_au_plus_haut_score = [liste_joueurs[x] for x in indices_du_plus_haut_score]
        return joueurs_au_plus_haut_score

    @staticmethod
    def trouver_indices_max(vecteur):
        valeur_max = max(vecteur)
        index_avec_plus_haute_valeur = []
        for i, j in enumerate(vecteur):
            if j == valeur_max:
                index_avec_plus_haute_valeur.append(i)
        return index_avec_plus_haute_valeur

    def determiner_joueur_suivant(self, liste_joueurs):
        """
        Méthode qui trouve qui est le joueur suivant et qui modifie l'attribut joueur_suivant de la partie.
        """
        if self.joueur_courant not in liste_joueurs:
            self.joueur_courant = self.joueur_suivant
        index_prochain_joueur_suivant = (liste_joueurs.index(self.joueur_courant) + self.sens + len(
            liste_joueurs)) % len(liste_joueurs)
        self.joueur_suivant = liste_joueurs[index_prochain_joueur_suivant]

    def reinitialiser_dés_joueurs(self):
        """
        Méthode qui réinitialise les dés des joueurs actifs en leur donnant 5 dés chacun.
        """
        for joueur in self.joueurs_actifs:
            joueur.reinitialiser_dés()

    def jouer_un_tour(self):
        self.joueur_courant.rouler_dés()
        self.message_narration = "Le joueur {} joue les dés suivants : {}\n\n"\
            .format(self.joueur_courant.identifiant, self.joueur_courant)
        self.gerer_dés_1_et_6()

        if self.verifier_si_fin_de_ronde():
            self.gagnant_ronde = self.joueur_courant
            self.message_narration += "\n\n\nLe joueur {} n'a plus de dé, il gagne la ronde\n\n"\
                .format(self.gagnant_ronde.identifiant)
            self.message_narration += "Les autres joueurs jouent leurs dés pour calculer\n" \
                                               "les points qu'ils donnent au joueur {}"\
                .format(self.gagnant_ronde.identifiant)

        self.passer_au_prochain_joueur(self.joueurs_actifs)

    def gerer_dés_1_et_6(self):
        nombre_1, nombre_6 = self.verifier_dés_joueur_courant_pour_1_et_6()
        self.afficher_messages_dés_1_et_6(nombre_1, nombre_6)
        self.deplacer_les_dés_1_et_6(nombre_1, nombre_6)

    def verifier_dés_joueur_courant_pour_1_et_6(self):
        """
        Méthode qui vérifie le nombre de dés de valeur 1 et 6 du joueur courant.
        Returns:
            int, int: nombre de dés de valeur 1 et 6
        """
        nombre_1, nombre_6 = self.joueur_courant.compter_1_et_6()
        return nombre_1, nombre_6

    def afficher_messages_dés_1_et_6(self, nombre_1, nombre_6):
        """
        Méthode qui affiche les messages de la présence de dés de valeur 1 et de dés de valeur 6 dans les dés du joueur
        courant. On affiche les messages que si le joueur a un dé de la valeur désignée.
        Args:
            nombre_1 (int): Nombre de dé(s) de valeur 1
            nombre_6 (int): Nombre de dé(s) de valeur 6
        """
        if nombre_1:
            self.message_narration += self.message_pour_dé_1(nombre_1)
        if nombre_6:
            self.message_narration += self.message_pour_dé_6(nombre_6)

    def message_pour_dé_1(self, nombre_1):
        """
        Méthode qui retourne le message sur le nombre de dé(s) de valeur 1. Par exemple, "Le joueur 2 a roulé 2 dés de
        valeur 1 et les retire du jeu."
        Args:
            nombre_1 (int): Nombre de dé(s) de valeur 1
        Returns:
            str: Message contenant le nombre de dé(s) retiré
        """
        return 'Le joueur {} retire {} dé{} de valeur 1 du jeu\n\n'.format(
                self.joueur_courant.identifiant, nombre_1, 's' if nombre_1 > 1 else '', 's' if nombre_1 > 1 else '')

    def message_pour_dé_6(self, nombre_6):
        """
        Méthode qui retourne le message sur le nombre de dé(s) de valeur 6. Par exemple, "Le joueur 4 a roulé 1 dé de
        valeur 6 et le passe au joueur suivant."
        Args:
            nombre_6 (int): Nombre de dé(s) de valeur 6
        Returns:
            str: Message contenant le nombre de dé(s) passé au suivant
        """
        return 'Le joueur {} passe {} dé{} de valeur 6 au joueur suivant\n\n'.format(
                self.joueur_courant.identifiant, nombre_6, 's' if nombre_6 > 1 else '', 's' if nombre_6 > 1 else '')

    def deplacer_les_dés_1_et_6(self, nombre_1, nombre_6):
        """
        Méthode qui déplace les dés de valeur 1 et de valeur 6 roulés par le joueur courant. Les dés de valeur 1 sont
        retirés du jeu (penser à une méthode de la classe joueur). Les dés de valeur 6 sont passés au joueur suivant.
        Args:
            nombre_1 (int): Nombre de dé(s) de valeur 1
            nombre_6 (int): Nombre de dé(s) de valeur 6
        """
        if nombre_1:
            # Si dé de valeur 1, les retirer.
            self.joueur_courant.retirer_dé(1)
        if nombre_6:
            # Si dé de valeur 6, les retirer.
            self.joueur_courant.retirer_dé(6)
            # Ajouter autant de dé de valeur 6 au joueur suivant
            for i in range(nombre_6):
                self.joueur_suivant.ajouter_un_dé()

    def verifier_si_fin_de_ronde(self):
        """
        Méthode qui vérifie si le joueur courant n'a plus de dé. Ceci signifie la fin de la ronde.
        Returns:
            bool: True, si le joueur courant n'a plus de dé. False autrement.
        """
        if len(self.joueur_courant.dés) == 0:
            return True
        else:
            return False

    def passer_au_prochain_joueur(self, liste_joueur):
        """
        Méthode qui change la valeur de l'attribut du joueur_courant et qui détermine le joueur suivant.
        """
        if self.joueur_suivant not in liste_joueur:
            self.determiner_joueur_suivant(liste_joueur)
        self.joueur_courant = self.joueur_suivant
        self.determiner_joueur_suivant(liste_joueur)
        self.message_tete_jeu = "Au tour du joueur {}".format(self.joueur_courant.identifiant)

    def passer_a_la_ronde_suivante(self):
        """
        Méthode qui incrémente le numéro de la ronde.
        """
        self.ronde += 1

    def terminer_ronde(self):
        """
        Méthode qui accomplit les actions de jeu en fin de ronde à l'aide d'autres méthodes de la classe.
        1. Tous les joueurs qui n'ont pas gagné la ronde jouent les dés qui leur restent.
        2. Afficher les messages des points donnés par les joueurs.
        3. Ajuster les points de perdants de la ronde et compter la somme des points destinés au gagnant.
        4. Ajuster les points du gagnant avec les points des perdants.
        5. Afficher le message qui annonce le nouveau score du gagnant.
        6. Retirer les joueurs sans points.
        """
        if self.tours_fin_de_ronde_joué <= len(self.joueurs_actifs):
            self.joueur_courant.rouler_dés()
            points = self.joueur_courant.calculer_points()
            self.message_narration = "Le joueur {} joue {} points" \
                .format(self.joueur_courant.identifiant, points)

            if points < self.joueur_courant.score:
                self.message_narration += " et les donnes au joueur {}".format(self.gagnant_ronde.identifiant)

                self.gagnant_ronde.score += points
                self.joueur_courant.score -= points
            else:
                self.message_narration += "\n\nLa somme des dés est égale ou supérieure à son score\n"
                self.message_narration += "Il donne {} point(s) au joueur {} et se retire de la partie"\
                    .format(self.joueur_courant.score, self.gagnant_ronde)

                self.gagnant_ronde.score += self.joueur_courant.score
                self.joueur_courant.score = 0

            self.tours_fin_de_ronde_joué += 1
            self.passer_au_prochain_joueur(self.joueurs_actifs)

        if self.tours_fin_de_ronde_joué == len(self.joueurs_actifs):
            self.retirer_joueurs_sans_points()
            if self.ronde < self.ronde_max:
                self.passer_a_la_ronde_suivante()
                self.preparer_debut_ronde()
            else:
                self.terminer_une_partie()

    def retirer_joueurs_sans_points(self):
        """
        Méthode qui vérifie si des joueurs actifs ont maintenant un score de 0. Seuls les joueurs ayant un score plus
        grand que zéro demeurent actifs. Advenant que le joueur suivant ne soit plus actif, le prochain joueur actif
        devient le nouveau joueur suivant.
        Returns:
            list: La liste des joueurs à retirer. (Cette valeur de retour ne devrait pas être utilisée dans le TP3, mais
            sera utile pour le TP4.
        """
        joueurs_à_conserver = []
        joueurs_à_retirer = []
        for joueur in self.joueurs_actifs:
            if joueur.score > 0:
                joueurs_à_conserver.append(joueur)
            else:
                joueurs_à_retirer.append(joueur)
                joueur.dés = []

        self.joueurs_actifs = joueurs_à_conserver

        if self.joueur_suivant not in self.joueurs_actifs:
            self.determiner_joueur_suivant(self.joueurs_actifs)

        return joueurs_à_retirer

    def terminer_une_partie(self):
        """
        Méthode qui fait les affichages de fin de partie. On informe les joueurs que le nombre maximal de rondes est
        atteint. Ensuite, ces affichages contiennent le bilan des points des joueurs et le message sur le ou les
        gagnants de la partie.
        """
        self.message_narration += "\n\n\nLe nombre maximal de rondes est atteint\n La partie est terminée!"
        self.message_tete_jeu = self.message_gagnants(self.determiner_liste_gagnants())
        self.partie_terminé = True

    def determiner_liste_gagnants(self):
        """
        Méthode qui détermine l'index des joueurs ayant le score le plus élevé. Considérer utiliser la méthode statique
        trouver_indices_max
        Returns:
            list: Liste contenant les indices des joueurs ayant le plus haut score. Il y a plus d'un joueur dans cette
            liste seulement s'il y a égalité.
        """
        liste_points_joueurs = []
        for joueur in self.joueurs:
            liste_points_joueurs.append(joueur.score)
        return Partie.trouver_indices_max(liste_points_joueurs)

    def message_gagnants(self, liste_index_gagnants):
        """
        Méthode qui assemble le message annonçant le gagnant (ou les gagnant en cas d'égalité). Par exemple, "Le joueur
        3 a gagné la partie!"
        Args:
            liste_index_gagnants (list): Liste contenant l'index (qui est l'identifiant) du ou des joueurs gagnants
        Returns:
            str: Message annonçant le gagnant.
        """
        if len(liste_index_gagnants) == 1:
            message = "Le joueur {} a gagné la partie!".format(self.joueurs[liste_index_gagnants[0]].identifiant)
        else:
            message = "Il y a égalité entre les joueurs {}!".format(" et ".join(
                str(self.joueurs[gagnant].identifiant) for gagnant in liste_index_gagnants))
        return message
