"""Lorsqu'un dossier contient un module __init__.py, c'est que nous le considérons comme
un "package", qui est une collection de modules regroupés dans un même projet.

Ce module spécial permet de faire:
from pymafia.partie import ...

Aucun code n'est nécessaire dans ce module spécial, sa présence est suffisante.
Si vous créez un package python dans Pycharm, vous obtiendrez automatiquement ce fichier.

"""
from pymafia.partie import Partie
from pymafia.joueur_humain import JoueurHumain
from pymafia.joueur_ordinateur import JoueurOrdinateur
from pymafia.de import Dé