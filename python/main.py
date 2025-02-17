from gameimports import *
pygame.init()


class Main:
    def __init__(self, wnw, wnh):
        self.wnw = wnw
        self.wnh = wnh
        self.window = pygame.display.set_mode((wnw, wnh))
        self.running = True
        self.location = 'WELCOME'
        self.coins = 0
        self.font_cache = {}
        self.fps = 70
        self.clock = pygame.time.Clock()
        self.playInstance = Game(self)
        self.pveInstance = PVEGame(self)
        self.jetons = []
        self.can_click = True  
        self.menu_data = None
        self.bg_music_playing = False

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
            if text['string']=="C'est au joueur ... de jouer !" and self.playInstance.game_over:
                text['display'] = False

            if text['name']=="Victory" and self.playInstance.game_over:
                text['string'] = f"Victoire du joueur {2 if self.playInstance.turn == 1 else 1} !"
                text['display'] = True

            if text['name']=="Victory" and self.pveInstance.game_over:
                if self.pveInstance.turn == 1:
                    text['string'] = "Défaite face à l'engine!"
                elif self.pveInstance.turn == 2:
                    text['string'] = "Victoire face à l'engine!"
                text['display'] = True
            

    

            if text['string']=="C'est au joueur ... de jouer !" and not self.playInstance.game_over:
                text['display'] = True

            if text['name']=="Victory" and not self.playInstance.game_over:
                text['string'] = f"Victoire du joueur {2 if self.playInstance.turn == 1 else 1} !"
                text['display'] = False

            if text['name']=="Victory" and not self.pveInstance.game_over:
                text['display'] = False



            if self.location == "INGAME":
                updated_text = text['string'].replace('...', str(self.playInstance.turn)) 
            elif self.location == "PVE":
                if text['name'] == "Prompt":
                    updated_text = "C'est à vous de jouer !" if self.pveInstance.turn == 1 else "C'est à l'engine de jouer !"
                else:
                    updated_text = text['string']
            else:
                updated_text = text['string'].replace('€', str(self.coins))
            font = self.get_font(text['size'])
            surf_text = font.render(updated_text, True, text['color'])
            if text['display']:
                self.window.blit(surf_text, (text['x'], text['y'])) 

    def __reinit_game__(self):
        REINIT_ALL_DATA()
        self.playInstance = Game(self)
        self.playInstance.update()
        self.location = "WELCOME"
        pygame.mixer.music.stop()
        self.bg_music_playing = False
        self.jetons = []
    
    def __reinit_PVE_game__(self):
        REINIT_ALL_DATA()
        self.pveInstance = PVEGame(self)
        self.pveInstance.update()
        self.location = "WELCOME"
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
    GameInstance = Main(900, 600)
    while GameInstance.running:
        GameInstance.__render__(next((menu for menu in ALL_MENUS if menu.__getInfo__()['Name'] == GameInstance.location), None))
        GameInstance.__listenToEvents__()
        pygame.display.flip()
