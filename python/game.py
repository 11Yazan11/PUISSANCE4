from data import *
import math
import pygame
import time
import threading


class Delay:
    def __init__(self, function):
        self.function = function
        self.running = False  # Track if a repeating interval is running

    def set_timeout(self, delay_time):
        """Execute the function after a delay."""
        timer = threading.Timer(delay_time, self.function)
        timer.start()

    def set_interval(self, interval_time):
        """Execute the function at regular intervals."""
        def interval_runner():
            while self.running:
                self.function()
                time.sleep(interval_time / 1000)  # Convert ms to seconds

        if not self.running:
            self.running = True
            thread = threading.Thread(target=interval_runner, daemon=True)
            thread.start()

    def stop_interval(self):
        """Stop a running interval."""
        self.running = False



    
        


class Bixel:
    def __init__(self, main, x, y, color, col):
        """Color is a tuple or list or rgb value only."""
        self.size = (400/7,444/7+4)
        self.game = main
        self.color = color
        self.COL = col
        self.gravity = 9.81 / self.game.fps
        self.grounded = False
        self.velocity_y = 0  # Current vertical velocity
        self.air_resistance = 0.009  # Air resistance (drag)
        self.elasticity = 0.8  # Coefficient of restitution (bounciness)
        self.rect = pygame.Rect(x, y, self.size[0], self.size[1])
        self.ground_level = 500-math.floor(self.size[1])

    def get_ground_level(self):
        """Find the nearest object below the player in the same column."""
        nearest = None
        for bixel in reversed(self.game.jetons):
            # Check if the `bixel` is in the same column
            if bixel.rect.x == self.rect.x:
                # Check if the `bixel` is directly below
                if bixel.rect.y >= self.rect.y + self.rect.h:
                    # Find the closest `bixel` below
                    if nearest is None or bixel.rect.y < nearest.rect.y:
                        nearest = bixel
    
        # Set the ground level based on the nearest `bixel`
        if nearest:
            self.ground_level = nearest.rect.y - nearest.rect.h
        else:
            self.ground_level = 500 - math.floor(self.size[1])

    def update(self):
        pygame.draw.rect(self.game.window, self.color, self.rect)
        pygame.draw.rect(self.game.window, self.darken_color(self.color), self.rect, 4)
        pygame.draw.rect(self.game.window, self.brigthen_color(self.color), self.rect, 2)
        if self.rect.y >= self.ground_level:
            self.velocity_y = -self.velocity_y * self.elasticity  # Bounce back with reduced energy
            self.rect.y = self.ground_level
            # Stop tiny oscillations when nearly at rest
            if abs(self.velocity_y) < 0.2:
                self.velocity_y = 0
                self.grounded = True
        elif not self.grounded:
            self.get_ground_level()
            self.velocity_y += self.gravity
            self.velocity_y -= self.air_resistance * self.velocity_y * abs(self.velocity_y)
            self.grounded = False

        self.rect.y += self.velocity_y

    def brigthen_color(self, color):
        """Brightens the given RGB color by increasing its values, clamped to a maximum of 255."""
        if not isinstance(color, (tuple, list)) or len(color) != 3:
            raise ValueError("Color must be a tuple or list with three elements representing RGB values.")
    
        # Increase each component by a fixed value, clamped to a maximum of 255
        brightened_color = tuple(min(c + 50, 255) for c in color)
        return brightened_color
    
    def darken_color(self, color):
        """Darkens the given RGB color by increasing its values, clamped to a minimum of 0."""
        if not isinstance(color, (tuple, list)) or len(color) != 3:
            raise ValueError("Color must be a tuple or list with three elements representing RGB values.")
    
        # Decrease each component by a fixed value, clamped to a minimum of 0
        darkened_color = tuple(max(c - 50, 0) for c in color)
        return darkened_color

    def handle_event(self, event):
        pass

    def destroy(self):
        if self in self.game.jetons:
            self.game.jetons.remove(self)



class Game:
    def __init__(self, main):
        self.main = main
        self.cursor_timer = 0
        self.waiting_for_cursor = False
        self.cursorOgVector = 0
        self.cursorExtOgVector = 0
        self.turn = 1
        self.jeton_color = lambda turn: (82, 71, 64) if turn == 1  else (40, 27, 56)
        self.game_grid = self.grille_init(7, 6)

    def horizontale(self, tab:list, joueur:int, w:int) -> bool:
            """Fonction qui renvoie True si le joueur a au moins 4 jetons alignés dans une ligne."""
            return any(
                all(row[i + j] == joueur for j in range(4))  
                for row in tab
                for i in range(w-3)) # Pour n'importe qu'elle ligne, vérifie les 4 jetons consécutifs dans la ligne en parcourant toutes les lignes et en s'assurant de rester dans ses limites

    def verticale(self, tab:list, joueur:int, w:int, h:int) -> bool:
        """Fonction qui renvoie True si le joueur a au moins 4 jetons alignés dans une colonne."""
        return any(
            all(tab[i + j][x] == joueur for j in range(4))  # Vérifie les 4 jetons consécutifs dans la colonne
            for x in range(w)  # Parcourt chaque colonne
            for i in range(h - 3)  # S'assure qu'il y a assez de place pour vérifier 4 jetons
        )

    def diagonale(self, tab:list, joueur:int, w:int, h:int) -> bool:
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
    
    def grille_init(self, w:int, h:int):
        """Initialise une nouvelle grille de jeu"""
        return [[0 for _ in range(w)] for _ in range(h)]
    
    
    def place_jeton(self, tab:list, colonne_index:int, joueur:int, h:int) -> list:
        """Fonction qui place un jeton du joueur (1 ou 2) dans la colonne. Elle renvoie la grille modifiée."""
        for row in range(h-1, -1, -1):  # Boucle de bas en haut
            if tab[row][colonne_index] == 0:  # Si la case est vide
                tab[row][colonne_index] = joueur  # On place le jeton
                break  # On sort de la boucle après avoir placé le jeton
        return tab
    
    def colonne_libre(self, tab:list, colonne_index:int) -> bool:
        """Fonction qui renvoie un booléen indiquant s'il est possible de mettre un jeton dans la colonne (indique si la colonne n'est pas pleine)"""
        return tab[0][colonne_index] == 0 # Si la première case (tout en haut) de la colonne est libre, alors la colonne est libre
    
    def gagne(self) -> bool:
        """Fonction qui renvoie True si le joueur a gagné"""
        turn = 2 if self.turn == 1 else 1
        return (self.horizontale(self.game_grid, turn, 7) or self.verticale(self.game_grid, turn, 7, 6) or self.diagonale(self.game_grid, turn, 7, 6))
    
    def update(self):
        if self.waiting_for_cursor:
            self.cursor_timer += 1
            if self.cursor_timer >= 25:
                elements = INGAMEMENU.__getInfo__()['Elements']
                cursorExt = next((element for element in elements if element['name'] == 'cursorExtension'), None)
                cursorExt['vector'][1] = 0
                cursorExt['y'] = cursorExt['ogY']
            if self.cursor_timer >= 100:
                self.cursor_timer = 0
                self.waiting_for_cursor = False
                elements = INGAMEMENU.__getInfo__()['Elements']
                cursor = next((element for element in elements if element['name'] == 'cursor'), None)
                cursorExt = next((element for element in elements if element['name'] == 'cursorExtension'), None)
                cursor['vector'] = [-self.cursorOgVector[0],self.cursorOgVector[1]] 
                cursorExt['vector'] = [-self.cursorExtOgVector[0], self.cursorExtOgVector[1]]
    
        if self.gagne():
            timeout = Delay(self.endgame)
            timeout.set_timeout(3)
            

    def endgame(self):
        self.main.location = 'WELCOME'
        self.game_grid = self.grille_init(7, 6)
        self.jetons = []

    def __handle_event__(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and not self.waiting_for_cursor:
            if 80 < event.pos[0] < 520 and 100 < event.pos[1] < 500 and self.main.location == "INGAME":
                elements = INGAMEMENU.__getInfo__()['Elements']
                cursor = next((element for element in elements if element['name'] == 'cursor'), None)
                cursorExt = next((element for element in elements if element['name'] == 'cursorExtension'), None)
                cursorP = cursor['attributes']
                cursorExtP = cursorExt['attributes']
                caseWidth = 442/7
                case = int(min(max(event.pos[0]-15, 120), 484)//caseWidth)
                if not self.colonne_libre(self.game_grid, case-1):
                    return
                cursorP.x = (case*caseWidth)+32
                cursorExtP.x = cursorP.x + 5
                self.cursorOgVector = cursor['vector']
                self.cursorExtOgVector = cursor['vector']
                cursor['vector'] = [0,0]
                cursorExt['vector'] = [0,1]
                self.main.jetons.append(Bixel(self.main, ((min(max(event.pos[0]-15, 120), 484)//caseWidth)*caseWidth)+19, cursorP.y+30, self.jeton_color(self.turn), case-1))
                self.game_grid = self.place_jeton(self.game_grid, case-1, self.turn, 6)
                self.turn = 1 if self.turn == 2 else 2
                self.waiting_for_cursor = True
               
                
                
                


        



