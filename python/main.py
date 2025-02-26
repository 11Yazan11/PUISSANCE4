from gameimports import *
pygame.init()


SERVER_URL = "http://localhost:5000"

script_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the script
info_file_path = os.path.join(script_dir, '..', 'appdata', 'myinfo.json')
rpldata_flag = False
players_in_main_lobby = []
SOCKET = None
PLAYERID = None
MYDATA = None
CURRENT_ONLINE_GAME_DATA = None




# Step 1: Connect to the server (POST request to '/connect')
def connect_to_server(player_name, player_id=None):
    
    if not player_id:
        # New player, only send the name to the server
        payload = {
            "name": player_name,
        }
    else:
        # Returning player, send both ID and name (name is retrieved from file)
        payload = {
            "ID": player_id,
            "name": player_name,
        }

    response = requests.post(f"{SERVER_URL}/connect", json=payload)
    

    if response.status_code == 200:
        data = response.json()
        return data  # Returning player data for further use (ID, name, etc.)
    else:
        print(f"Failed to connect: {response.json()}")
        return None



if os.path.exists(info_file_path):
    with open(info_file_path, 'r') as file:
        data = json.load(file)
        PLAYERNAME = data.get('name')
        PLAYERID = data.get('ID')
else:
    data = {
        "ID": None,
        "name": None
    }

# If there's no name and ID, this is the player's first time
if PLAYERNAME is None or PLAYERID is None:
    PLAYERNAME = input("Before starting this game for the first time, you may want to enter a name. You will not be able to change it: ")
    print("Please wait while we connect you to the server...")
    PLAYERNAME = PLAYERNAME.strip('"')  # Remove any quotes around the name
    data['name'] = PLAYERNAME  # Save the player's name
    data['ID'] = None  # Keep ID as None until server responds

    # Send the player's name to the server to create the account
    player_data = connect_to_server(player_name=PLAYERNAME)
    
    if player_data:
        # Update the local player info with the returned ID
        data['ID'] = player_data['ID']
        # Save the player data to the JSON file for future use
        with open(info_file_path, 'w') as file:
            json.dump(data, file, indent=4)
else:
    print(f"Welcome back, {PLAYERNAME}!")
    print("Please wait while we connect you to the server...")
    connect_to_server(player_name=PLAYERNAME, player_id=PLAYERID)
    


def request_player_data():
    if os.path.exists(info_file_path):
        with open(info_file_path, 'r') as file:
            data = json.load(file)
            plid = data.get('ID')
            SOCKET.emit("request_player_data", {"ID": plid})


def request_inlobby_players():
    SOCKET.emit("request_inlobby_players")
    


def join_main_lobby():
    SOCKET.emit("join_main_lobby", {"ID": PLAYERID})

    


def run_socket_client():
    # Initialize SocketIO client 
    global SOCKET, players_in_main_lobby
    SOCKET = Client(logger=True, engineio_logger=True)

    
    # Connect to the server
    SOCKET.connect(SERVER_URL)


    @SOCKET.on("receive_player_data")
    def on_receive_player_data(data):
        global rpldata_flag, MYDATA
        if "error" in data:
            print("Error:", data["error"])
        else:
            rpldata_flag = True
            MYDATA = data

    @SOCKET.on("start_game")
    def on_start_game(data):
        print('Starting a game.')
        global GameInstance, CURRENT_ONLINE_GAME_DATA
        CURRENT_ONLINE_GAME_DATA = data
        print(f"Launching game {CURRENT_ONLINE_GAME_DATA}...")
        GameInstance.location = "ONLINE"

    @SOCKET.on("joined_main_lobby")
    def on_joined_main_lobby():
        request_inlobby_players()

    @SOCKET.on("receive_inlobby_players")
    def on_receive_inlobby_players(data):
        global players_in_main_lobby
        players_in_main_lobby = data




    request_player_data()
    SOCKET.wait()
    




def disconnect_from_server(player_id, socket=None):
    payload = {
        "ID": player_id
    }
    response = requests.post(f"{SERVER_URL}/leave", json=payload)

    if response.status_code == 200:
        
        # Now disconnect from SocketIO server
        if socket is not None:
            socket.disconnect()
            
    else:
        print(f"Failed to disconnect from HTTP server: {response.json()}")








































class Main:
    def __init__(self, wnw, wnh, globalscore, money, skins, name):
        self.wnw = wnw
        self.wnh = wnh
        self.window = pygame.display.set_mode((wnw, wnh))
        self.running = True
        self.location = 'WELCOME'
        self.font_cache = {}
        self.fps = 70
        self.clock = pygame.time.Clock()
        self.playInstance = Game(self)
        self.pveInstance = PVEGame(self)
        self.jetons = []
        self.can_click = True  
        self.menu_data = None
        self.bg_music_playing = False
        self.globalscore = globalscore
        self.coins = money
        self.name = name
        self.skins = skins

    def get_font(self, size):
        if size not in self.font_cache:
            self.font_cache[size] = pygame.font.Font(None, size)
        return self.font_cache[size]

    def Btnplay(self):
        self.location = 'GAMECHOICE'

    def Btnpvp(self):
        self.location = 'INGAME'
        pygame.mixer.music.stop()
        self.bg_music_playing = False
    
    def Btnpve(self):
        self.location = 'PVE'
        pygame.mixer.music.stop()
        self.bg_music_playing = False

    def Btnmainlobby(self):
        join_main_lobby()
        self.location = 'MAINLOBBY'
        pygame.mixer.music.stop()
        self.bg_music_playing = False

    def Btnbfgc(self):
        self.location = 'WELCOME'

    def Btnexit(self):
        timeout = Delay(self.__reinit_game__)
        timeoutpve = Delay(self.__reinit_PVE_game__)
        timeoutpve.set_timeout(0.1)
        timeout.set_timeout(0.1)

    def __drawElems__(self, elems):
        for elem in elems:
            attr = elem['attributes']
            color = elem['color']
            if elem['clickable']:
                if pygame.mouse.get_pressed()[0]:
                    time.sleep(0.1)
                    self.can_click = False
                    if elem['attributes'].collidepoint(pygame.mouse.get_pos()):
                       getattr(self, elem['clickable'])()
                else:
                    if not pygame.mouse.get_pressed()[0]:
                        self.can_click = True
                    if elem['attributes'].collidepoint(pygame.mouse.get_pos()):
                        pygame.draw.rect(self.window, elem['color'], (attr.x, attr.y, attr.w, attr.h), 4, 10) # hovering: black frame
 
            else:
                if elem['texture'] is None:
                    if elem['name'] == "border":
                        pygame.draw.rect(self.window, color, (attr.x, attr.y, attr.w, attr.h), 10)
                    else:
                        pygame.draw.rect(self.window, color, (attr.x, attr.y, attr.w, attr.h))
                else:
                    try:
                        texture = pygame.image.load(elem['texture']).convert_alpha()
                        texture = pygame.transform.scale(texture, (attr.w, attr.h))
                        self.window.blit(texture, (attr.x, attr.y))
                    except:
                        print('Image file link invalid.')

            if elem['vector'][0] > 0:
                if elem["attributes"].x >= elem["ogX"] + elem["limit"][0]:
                    elem['vector'][0] *= -1
            if elem['vector'][0] < 0:
                if elem["attributes"].x <= elem["ogX"] - elem["limit"][0]:
                    elem['vector'][0] *= -1
            
            if elem['vector'][1] > 0:
                if elem["attributes"].y >= elem["ogY"] + elem["limit"][1]:
                    elem['vector'][1] *= -1
            if elem['vector'][1] < 0:
                if elem["attributes"].y <= elem["ogY"] - elem["limit"][1]:
                    elem['vector'][1] *= -1

            elem["attributes"].x += elem["vector"][0]
            elem["attributes"].y += elem["vector"][1]

    def __drawTexts__(self, texts):
        for text in texts:
            if text['name'] is not None:
                if "todelete" in text['name']:
                    MAINLOBBYMENU.__removeText__(text['name'])
            if text['name']=="Prompt" and self.playInstance.game_over and self.location == "INGAME":
                text['display'] = False

            if text['name']=="Prompt" and self.pveInstance.game_over and self.location == "PVE":
                text['display'] = False


            if text['name']=="Victory" and self.playInstance.game_over and self.location == "INGAME":
                text['string'] = f"Victoire du joueur {2 if self.playInstance.turn == 1 else 1} !"
                text['display'] = True

            if text['name']=="Victory" and self.pveInstance.game_over and self.location == "PVE":
                if self.pveInstance.turn == 1:
                    text['string'] = "Défaite face à l'engine!"
                    text['color'] = (200, 0, 50)
                elif self.pveInstance.turn == 2:
                    text['string'] = "Victoire face à l'engine!"
                text['display'] = True
            

    

            if text['name']=="Prompt" and not self.playInstance.game_over and self.location == "INGAME":
                text['display'] = True
            if text['name']=="Prompt" and not self.pveInstance.game_over and self.location == "PVE":
                text['display'] = True
            
           

            if text['name']=="Victory" and not self.playInstance.game_over and self.location == "INGAME":
                text['string'] = f"Victoire du joueur {2 if self.playInstance.turn == 1 else 1} !"
                text['display'] = False

            if text['name']=="Victory" and not self.pveInstance.game_over and self.location == "PVE":
                text['display'] = False


            if self.location == "WELCOME":
                if text['name'] == "Myscore":
                    text['string'] = text['string'].replace('<score>', str(self.globalscore))

            if self.location == "MAINLOBBY":
                if text['name'] == "mainlobbyplayers":
                    text['string'] = 'In Queue:'
                    i = 1
                    for player in players_in_main_lobby:
                        PLAYERID = MYDATA['ID']
                        if player['ID'] == PLAYERID:
                            if player['name'] == self.name:
                                player['name'] = f"{player['name']} (vous)"
                        MAINLOBBYMENU.__addText__(f"{player['name']}", 445, 220 + i*30, (166, 201, 85), 18, center=True, name=f"todelete-{i}")
                        i += 1

            if self.location == "INGAME":
                updated_text = text['string'].replace('...', str(self.playInstance.turn)) 

            if self.location == "PVE":
                if text['name'] == "Prompt":
                    updated_text = "C'est à vous de jouer !" if self.pveInstance.turn == 1 else "C'est à l'engine de jouer !"
                else:
                    updated_text = text['string']
            else:
                updated_text = text['string'].replace('€', f"{str(self.coins)}K")
                


            font = self.get_font(text['size'])
            surf_text = font.render(updated_text, True, text['color'])
            if text['display']:
                if text['center'] == True:
                    self.window.blit(surf_text, (text['x'] - surf_text.get_width()/2, text['y']))
                else:
                    self.window.blit(surf_text, (text['x'], text['y']))

    def __drawInputs__(self, inputs):
        for input in inputs:
            font = self.get_font(input['txtsize'])
            text = input["placeholder"].replace("<yourname>", self.name)
            surf_text = font.render(text, True, input['txtcolor'])
            pygame.draw.rect(self.window, input['bgcolor'], (input['attributes'].x, input['attributes'].y, input['attributes'].w, input['attributes'].h))
            self.window.blit(surf_text, (input['attributes'].x + input['attributes'].w/2 - surf_text.get_width()/2, input['attributes'].y + input['attributes'].h/2 - surf_text.get_height()/2))

            if not input['focused']: # hovering
                if input['attributes'].collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.rect(self.window, (20, 100, 50), (input['attributes'].x, input['attributes'].y, input['attributes'].w, input['attributes'].h), 4) # hovering: white frame
                else:
                    pygame.draw.rect(self.window, (0, 0, 0), (input['attributes'].x, input['attributes'].y, input['attributes'].w, input['attributes'].h), 4)

            # Put a little dark layer over it if not focused.

                

    def __reinit_game__(self):
        REINIT_ALL_DATA()
        self.playInstance.cursor_timer = 101
        self.playInstance.update()
        self.playInstance = Game(self)
        self.playInstance.update()
        self.location = "GAMECHOICE"
        pygame.mixer.music.stop()
        self.bg_music_playing = False
        self.jetons = []
    
    def __reinit_PVE_game__(self):
        REINIT_ALL_DATA()
        self.pveInstance.cursor_timer = 101
        self.pveInstance.update()
        self.pveInstance = PVEGame(self)
        self.pveInstance.update()
        self.location = "GAMECHOICE"
        pygame.mixer.music.stop()
        self.bg_music_playing = False
        self.jetons = []

    def __render__(self, menu):
        if not pygame.mouse.get_pressed()[0]:
            self.clicking = False
        self.menu_data = menu.__getInfo__()
        menu_data = self.menu_data
        self.window.fill(menu_data['Bg'])
        if menu_data['Img'] is not None:
            img = pygame.image.load(menu_data['Img']).convert_alpha()
            img = pygame.transform.scale(img, (900, 600))
            self.window.blit(img, (0, 0))
        if menu_data['Sound'] is not None:
            if not self.bg_music_playing:
                pygame.mixer.music.load(menu_data['Sound'])
                pygame.mixer.music.play(-1)
                self.bg_music_playing = True
                
        pygame.display.set_caption(f'PROJECT GALAXY MADNESS - {menu_data['Name']}')

        for bixel in self.jetons:
                bixel.update()


        if self.location == "MAINLOBBY":
            pass
        if self.location == "WELCOME":
            self.jetons = []

        if menu_data['Name'] == 'INGAME':
            self.playInstance.update()
            if self.playInstance.game_over:
                timeout = Delay(self.__reinit_game__)
                timeout.set_timeout(5)

        if menu_data['Name'] == 'PVE':
            self.pveInstance.update()
            if self.pveInstance.game_over:
                timeout = Delay(self.__reinit_PVE_game__)
                timeout.set_timeout(5)

           

        self.__drawElems__(menu_data['Elements'])
        self.__drawTexts__(menu_data['Texts'])
        self.__drawInputs__(menu_data['Inputs'])
        self.clock.tick(self.fps)

    def __listenToEvents__(self):
        for event in pygame.event.get():
            if self.location == "INGAME":
                self.playInstance.__handle_event__(event)
            if self.location == "PVE":
                self.pveInstance.__handle_event__(event)
            if event.type == pygame.QUIT:
                self.running = False




if __name__ == "__main__":
    socket_thread = threading.Thread(target=run_socket_client)
    socket_thread.start()
    while rpldata_flag == False:
        pass
    print("Connected!")
    GameInstance = Main(900, 600, MYDATA['score'], MYDATA['money'], MYDATA['skins'], MYDATA['name'])
    while GameInstance.running:
        PLAYERID = MYDATA['ID']
        GameInstance.__render__(next((menu for menu in ALL_MENUS if menu.__getInfo__()['Name'] == GameInstance.location), None))
        GameInstance.__listenToEvents__()
        pygame.display.flip()

    PLAYERID = MYDATA['ID']
    disconnect_from_server(PLAYERID, SOCKET)
    print("Disconnected!")
    pygame.quit()
