# IMPORTS
import math
import os
#----------

# METHODES ET FONCTIONS DU CODE
def grille_init(w:int, h:int):
    """Initialise une nouvelle grille de jeu"""
    return [[0 for _ in range(w)] for _ in range(h)]

def affiche_grille(tab:list) -> None:
    """Affiche la grille dans un format lisible et esthétique."""
    separator_length = ((w * 4) + 1)
    os.system('cls' if os.name == 'nt' else 'clear')  # Efface l'écran pour une mise à jour visuelle
    print('-' * separator_length) # Ligne de séparation initiale
    print('+' + ('---+' * w)) # Ligne de spéparation intermédaire
    for row in tab:
        print('| ' + ' | '.join(str(cell) for cell in row) + ' |')
        print('+' + ('---+' * w)) # Ligne de spéparation intermédaire
    print('-' * separator_length)  # Ligne de séparation finale
    print()
    print()

    # Demander à l'utilisateur de saisir une colonne
    # Texte coloré dans le terminal
    print(f"\033[1;31mLe joueur {turn} doit donner une colonne dans laquelle placer son jeton. (de 0 à {w-1}) : \033[0m")
    colonne = int(input(">>> "))
    return colonne



def colonne_libre(tab:list, colonne_index:int) -> bool:
    """Fonction qui renvoie un booléen indiquant s'il est possible de mettre un jeton dans la colonne (indique si la colonne n'est pas pleine)"""
    return tab[0][colonne_index] == 0 # Si la première case (tout en haut) de la colonne est libre, alors la colonne est libre

def place_jeton(tab:list, colonne_index:int, joueur:int) -> list:
    """Fonction qui place un jeton du joueur (1 ou 2) dans la colonne. Elle renvoie la grille modifiée."""
    for row in range(h-1, -1, -1):  # Boucle de bas en haut
        if tab[row][colonne_index] == 0:  # Si la case est vide
            tab[row][colonne_index] = joueur  # On place le jeton
            break  # On sort de la boucle après avoir placé le jeton
    return tab

def horizontale(tab:list, joueur:int) -> bool:
    """Fonction qui renvoie True si le joueur a au moins 4 jetons alignés dans une ligne."""
    return any(
        all(row[i + j] == joueur for j in range(4))  
        for row in tab 
        for i in range(w-3)) # Pour n'importe qu'elle ligne, vérifie les 4 jetons consécutifs dans la ligne en parcourant toutes les lignes et en s'assurant de rester dans ses limites

def verticale(tab:list, joueur:int) -> bool:
    """Fonction qui renvoie True si le joueur a au moins 4 jetons alignés dans une colonne."""
    return any(
        all(tab[i + j][x] == joueur for j in range(4))  # Vérifie les 4 jetons consécutifs dans la colonne
        for x in range(w)  # Parcourt chaque colonne
        for i in range(h - 3)  # S'assure qu'il y a assez de place pour vérifier 4 jetons
    )

def diagonale(tab:list, joueur:int) -> bool:
    """Fonction qui renvoie True si le joueur a au moins 4 jetons alignés sur une diagonale."""
    return any(
        all(tab[i + j][x + j] == joueur for j in range(4))  # Diagonale descendante
        for x in range(w - 3)  # Limite des colonnes pour la diagonale descendante
        for i in range(h - 3)  # Limite des lignes pour la diagonale descendante
    ) or any(
        all(tab[i + j][x - j] == joueur for j in range(4))  # Diagonale montante
        for x in range(3, w)  # Limite des colonnes pour la diagonale montante
        for i in range(h - 3)  # Limite des lignes pour la diagonale montante
    )

def gagne(tab:list, joueur:int) -> bool:
    """Fonction qui renvoie True si le joueur a gagné"""

    # Pour l'instant, les conditions ci-dessous ne chequent pas des victoires doubles ou triples.
    if horizontale(game_grid,turn):
        print(f"VICTOIRE HORIZONTALE DU JOUEUR {turn}")
        return True
    elif verticale(game_grid,turn):
        print(f"VICTOIRE VERTICALE DU JOUEUR {turn}")
        return True
    elif diagonale(game_grid, turn):
        print(f"VICTOIRE DIAGONALE DU JOUEUR {turn}")
        return True
    else:
        return False
    

def tour_joueur():
    pass

def egalite():
    pass

def jouer():
    if False: #If a player plays somewhere and the COL IS FREE
        game_grid = place_jeton()
        affiche_grille(game_grid)
#----------

# CONSTANTES ET VARIABLES
w = 7
h = 6
turn = 1
game_grid = grille_init(w, h)
#----------


# JEU ET BOUCLE DE JEU
if __name__ == "__main__":
    affiche_grille(game_grid)
    jouer(game_grid)
        

        
#----------