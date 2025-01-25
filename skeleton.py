# IMPORTS
import os
import time
#----------

# METHODES ET FONCTIONS DU CODE
def grille_init(w:int, h:int):
    """Initialise une nouvelle grille de jeu"""
    return [[0 for _ in range(w)] for _ in range(h)]

def affiche_grille(tab:list, joueur=None, egalite=False) -> None:
    """Affiche la grille dans un format lisible et esthétique."""
    #IL EST POSSIBLE D'UTILISER CETTE METHODE POUR SEULEMENT AFFICHER LA GRILLE SANS DEMANDE DE JEU
    separator_length = ((w * 4) + 1)
    os.system('cls' if os.name == 'nt' else 'clear')  # Efface l'écran pour une mise à jour visuelle
    print('-' * separator_length) # Ligne de séparation initiale
    print('+' + ('---+' * w)) # Ligne de spéparation intermédaire
    for row in tab:
        if egalite:
            print('\033[1;33m| ' + ' | '.join(" " if int(cell)==0 else "X" if int(cell)==1 else "O" for cell in row) + ' |')
            print('+' + ('---+' * w)) # Ligne de spéparation intermédaire
        else:
            print('| ' + ' | '.join(" " if int(cell)==0 else "X" if int(cell)==1 else "O" for cell in row) + ' |')
            print('+' + ('---+' * w)) # Ligne de spéparation intermédaire

    print('\033[0m-' * separator_length)  # Ligne de séparation finale
    print()
    print("Player 1 : X ")
    print("Player 2 : O")
    print()


    # Demander à l'utilisateur de saisir une colonne
    # Texte coloré dans le terminal
    if joueur is not None:
        print(f"\033[1;31mLe joueur {joueur} doit donner une colonne dans laquelle placer son jeton. (de 1 à {w}) : \033[0m")
        colonne = input(">>> ")
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

def gagne(tab:list, turn:int) -> bool:
    """Fonction qui renvoie True si le joueur a gagné"""
    return (horizontale(tab, turn) or verticale(tab, turn) or diagonale(tab, turn))
    

def tour_joueur(tab:list, joueur:int) -> list:
    has_played = False
    if gagne(tab, 1):
        affiche_grille(tab)
        print(f"\033[1;32mVICTOIRE DU JOUEUR 1!\033[0m")
        return "end"
    elif gagne(tab, 2):
        affiche_grille(tab)
        print(f"\033[1;32mVICTOIRE DU JOUEUR 2!\033[0m")
        return "end"
    elif egalite(tab):
        affiche_grille(tab, egalite=True)
        print(f"\033[1;35mOOPS, EGALITE! PAS DE VAINQEUR!\033[0m")
        return "end"

    while not has_played:
        col = affiche_grille(tab, joueur)
        try:
            col = int(col) - 1
            if not (0 <= col < w):
                print(f"\033[1;33mVeuillez entrer un numéro de colonne valide (entre 1 et {w}).\033[0m")
                time.sleep(3)
            elif colonne_libre(tab, col):
                new_tab = place_jeton(tab, col, joueur)
                print("\033[1;34mCoup joué\033[0m")
                time.sleep(1)
                return new_tab
            else:
                print("\033[1;33mCette colonne est pleine, choisissez-en une autre.\033[0m")
                time.sleep(3)
        except ValueError:
            print("\033[1;33mVeuillez entrer un entier valide.\033[0m")
            time.sleep(3)
                
            
        

def egalite(tab):
    return all(not colonne_libre(tab, col) for col in range(0, w))

def jouer(tab, joueur):
    while True:
        tab = tour_joueur(tab, joueur)
        if tab=="end":
            return
        joueur = 2 if joueur == 1 else 1
#----------

# CONSTANTES ET VARIABLES
w = 7
h = 6
initial_turn = 1
game_grid = grille_init(w, h)
#----------


# JEU ET BOUCLE DE JEU
if __name__ == "__main__":
    jouer(game_grid, initial_turn)
    print("---------------------")
    print()
    print("FIN DU JEU!")
#----------