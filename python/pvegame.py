from game import *
from data import *
from threading import *
from together import Together
import requests

client = Together(api_key="e3f1166e1e48c5cbcb9c963fb72505ee7283c6bffdfab18abc721bb3e844635f")

class PVEGame(Game):
    def __init__(self, main):
        super().__init__(main)
        self.ai_turn_pending = False
    
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

        if self.ai_turn_pending and not self.waiting_for_cursor and not self.game_over:
            self.start_ai_turn()
             
                        
        if self.waiting_for_cursor:
            elements = PVEMENU.__getInfo__()['Elements']
            cursorExt = next((element for element in elements if element['name'] == 'cursorExtension'), None)
            if cursorExt['attributes'].y == cursorExt['ogY']:
                self.cursor_timer += 1
            
            if self.cursor_timer >= 2:
                cursorExt['vector'] = [0, 0]

            if self.cursor_timer >= 100:
                self.cursor_timer = 0
                self.waiting_for_cursor = False
                elements = PVEMENU.__getInfo__()['Elements']
                cursor = next((element for element in elements if element['name'] == 'cursor'), None)
                cursorExt = next((element for element in elements if element['name'] == 'cursorExtension'), None)
                cursor['vector'] = [-self.cursorOgVector[0],self.cursorOgVector[1]] 
                cursorExt['vector'] = [-self.cursorExtOgVector[0], self.cursorExtOgVector[1]]


    def start_ai_turn(self):
        # Start AI turn in a separate thread
        ai_thread = Thread(target=self.ai_turn)
        ai_thread.start()
        self.ai_turn_pending = False  # Reset the flag once the AI turn starts

    def ai_turn(self):
        # Convert game grid to string format
        if self.turn != 2: return
        board_str = "".join(["".join(map(str, row)) for row in self.game_grid])

        url = "https://kevinalbs.com/connect4/back-end/index.php/getMoves"
        params = {'board_data': board_str}
        response = requests.get(url, params=params)
    
        if response.status_code == 200:
            ai_move = int(max(response.json(), key=response.json().get))

        else:
            print("Error retrieving a move from the engine.")
            print(response.status_code)
            return
        

        

        # Place the AI move on the board
        if self.colonne_libre(self.game_grid, ai_move):
            row = next((r for r in range(5, -1, -1) if self.game_grid[r][ai_move] == 0), -1)
            bixeltoappend = Bixel(self.main, ((ai_move+1) * (442/7)) + 19, 100, self.jeton_color(2), ai_move, (row, ai_move), os.path.join(script_dir, "..", "images", "p4", "skins", "goofy", "blue-goofy.png"))
            self.main.jetons.append(bixeltoappend)
            self.game_grid = self.place_jeton(self.game_grid, ai_move, 2, 6)
            self.turn = 1  # Give turn back to the player
            elements = PVEMENU.__getInfo__()['Elements']
            cursor = next((element for element in elements if element['name'] == 'cursor'), None)
            cursorExt = next((element for element in elements if element['name'] == 'cursorExtension'), None)
            cursorP = cursor['attributes']
            cursorExtP = cursorExt['attributes']
            caseWidth = 442/7
            cursorP.x = ((ai_move+1)*caseWidth)+32
            cursorExtP.x = cursorP.x + 5
            self.cursorOgVector = cursor['vector']
            self.cursorExtOgVector = cursor['vector']
            cursor['vector'] = [0,0]
            cursorExt['vector'] = [0,1]
            self.waiting_for_cursor = True
            


    def __handle_event__(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and not self.waiting_for_cursor and not self.game_over and self.turn == 1:
            if 80 < event.pos[0] < 520 and 100 < event.pos[1] < 500 and self.main.location == "PVE":
                elements = PVEMENU.__getInfo__()['Elements']
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
                self.ai_turn_pending = True  # Set the flag that AI should take its turn
                self.waiting_for_cursor = True