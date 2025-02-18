from data import *
from bixel import *
from delay import Delay
script_dir = os.path.dirname(__file__)


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
        self.game_over = False

    def horizontale(self, tab: list, joueur: int, w: int, h:int):
        """Renvoie les positions des jetons gagnants en cas de victoire horizontale, sinon None."""
        for row_index, row in enumerate(tab):
            for i in range(w - 3):
                if all(row[i + j] == joueur for j in range(4)):
                    return [(row_index, i + j) for j in range(4)]
        return None


    def verticale(self, tab: list, joueur: int, w: int, h: int):
        """Renvoie les positions des jetons gagnants en cas de victoire verticale, sinon None."""
        for x in range(w):
            for i in range(h - 3):
                if all(tab[i + j][x] == joueur for j in range(4)):
                    return [(i + j, x) for j in range(4)]
        return None


    def diagonale(self, tab: list, joueur: int, w: int, h: int):
        """Renvoie les positions des jetons gagnants en cas de victoire diagonale, sinon None."""
        for x in range(w - 3):
            for i in range(h - 3):
                if all(tab[i + j][x + j] == joueur for j in range(4)):  # Diagonale descendante
                    return [(i + j, x + j) for j in range(4)]
        for x in range(3, w):
            for i in range(h - 3):
                if all(tab[i + j][x - j] == joueur for j in range(4)):  # Diagonale montante
                    return [(i + j, x - j) for j in range(4)]
        return None

    
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
    
    def gagne(self):
        turn = 2 if self.turn == 1 else 1
        for check in [self.horizontale, self.verticale, self.diagonale]:
            winning_positions = check(self.game_grid, turn, 7, 6)
            if winning_positions:
                return winning_positions
        return None

    
    def change_color(self, bixel):
        if bixel.image is not None:
            bixel.set_image(os.path.join(script_dir, "..", "images", "p4", "skins", "goofy", "green-goofy.png"))
            bixel.color = (0, 100, 0)
  
    def update(self):
        winning_positions = self.gagne()
        if winning_positions and self.game_over == False:
            self.game_over = True
            for pos in winning_positions:
                row, col = pos
                for bixel in self.main.jetons:
                    if bixel.grid_position == (row, col):
                        timeout = Delay(self.change_color, bixel)
                        timeout.set_timeout(1)

        
             
                        
        if self.waiting_for_cursor:
            elements = INGAMEMENU.__getInfo__()['Elements']
            cursorExt = next((element for element in elements if element['name'] == 'cursorExtension'), None)
            if cursorExt['attributes'].y == cursorExt['ogY']:
                self.cursor_timer += 1
            
            if self.cursor_timer >= 2:
                cursorExt['vector'] = [0, 0]

            if self.cursor_timer >= 70:
                self.cursor_timer = 0
                self.waiting_for_cursor = False
                elements = INGAMEMENU.__getInfo__()['Elements']
                cursor = next((element for element in elements if element['name'] == 'cursor'), None)
                cursorExt = next((element for element in elements if element['name'] == 'cursorExtension'), None)
                cursor['vector'] = [-self.cursorOgVector[0],self.cursorOgVector[1]] 
                cursorExt['vector'] = [-self.cursorExtOgVector[0], self.cursorExtOgVector[1]]
            
   
        
         

        

    def __handle_event__(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and not self.waiting_for_cursor and not self.game_over:
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
                row = next((r for r in range(5, -1, -1) if self.game_grid[r][case-1] == 0), -1)
                col = case - 1
                color = 'red' if self.turn == 1 else 'blue' 
                bixeltoappend = Bixel(self.main, ((min(max(event.pos[0]-15, 120), 484)//caseWidth)*caseWidth)+19, cursorP.y+30, self.jeton_color(self.turn), case-1, (row, col), os.path.join(script_dir, "..", "images", "p4", "skins", "goofy", f"{color}-goofy.png"))
                self.main.jetons.append(bixeltoappend)
                self.game_grid = self.place_jeton(self.game_grid, case-1, self.turn, 6)
                self.turn = 1 if self.turn == 2 else 2
                self.waiting_for_cursor = True
               
                
                
                


        



