# IMPORTS
import math
import os
#----------

# METHODES ET FONCTIONS DU CODE
def grille_init():
    """Initialise une nouvelle grille de jeu"""
    return [[0 for _ in range(7)] for _ in range(6)]

def affiche_grille(tab:list) -> None:
    """Affiche la grille dans un format lisible et esthétique."""
    os.system('cls' if os.name == 'nt' else 'clear')  # Efface l'écran pour une mise à jour visuelle
    print('-' * 29) 
    for row in tab:
        print('| ' + ' | '.join(str(cell) if cell != 0 else '.' for cell in row) + ' |')
    print('-' * 29)  # Ligne de séparation

def colonne_libre():
    pass

def place_jeton():
    affiche_grille(game_grid)

def horizontale():
    pass

def verticale():
    pass

def diagonale():
    pass

def gagne():
    pass

def tour_joueur():
    pass

def egalite():
    pass

def jouer():
    pass
#----------

# CONSTANTES ET VARIABLES
game_grid = grille_init()
#----------


# JEU ET BOUCLE DE JEU
if __name__ == "__main__":
    affiche_grille(game_grid)
    while True:
        pass 
        

        
#----------