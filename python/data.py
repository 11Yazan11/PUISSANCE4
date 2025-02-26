from menues import Menu
import os
from datetime import datetime

from datetime import datetime

current_month_abbr = datetime.now().strftime("%b")






script_dir = os.path.dirname(__file__)


WELCOMEMENU_OBJS = [[10, 0, 880, 10, (0, 0, 0), False, None, (0, 0)],
                    [0, 0, 10, 590, (0, 0, 0), False, None, (0, 0)],
                    [890, 0, 10, 590, (0, 0, 0), False, None, (0, 0)],
                    [0, 590, 900, 10, (0, 0, 0), False, None, (0, 0)],
                    [310, 358, 287, 103, (0, 0, 0), 'Btnplay', None, (0, 0), True],
                    [17, 105, 220, 340, (50, 20, 20), False, None, (0, 0)],
                    [610, 85, 250, 150, (50, 20, 20), False, None, (0, 0)],
                    [370, 125, (400/7)*3, (444/7+4)*3, (0, 0, 0), False, os.path.join(script_dir, "..", "images", "p4", "default.png"), (0, 2), (0, 8)],
                    ]
def reinitWelcome():
    global WELCOMEMENU
    WELCOMEMENU = Menu('WELCOME', (10, 10, 10), os.path.join(script_dir, "..", "images", "p4", "Menus", "mBase.png"), song=os.path.join(script_dir, "..", "sounds", "home.mp3")) 
    for obj in WELCOMEMENU_OBJS:
        WELCOMEMENU.__addObject__({"x":obj[0], "y":obj[1],
                               "w":obj[2], "h":obj[3],
                               "c":obj[4], "t":obj[6],
                               "vecxy":obj[7], "lim":obj[-1] if len(obj) == 9 else obj[-2] if len(obj) == 10 else None,
                               "name":obj[-1] if len(obj) == 10 else None}, 
                               clickable=obj[5])
    WELCOMEMENU.__addText__('€', 63, 34, (50, 50, 50), 40, True, 'GeneralMoneyDisplay', center=True)
    WELCOMEMENU.__addText__(f'Monthly Scores ({current_month_abbr}.)', 27, 125, (200, 200, 210), 28, True, 'Scores')
    WELCOMEMENU.__addText__('---------------------------', 31, 150, (200, 200, 210), 30, True)
    WELCOMEMENU.__addText__('1. | <name> ~~~ <score>', 29, 200, (160, 150, 21), 24, True, 'Player1score')
    WELCOMEMENU.__addText__('2. | <name> ~~~ <score>', 29, 240, (100, 100, 100), 24, True, 'Player2score')
    WELCOMEMENU.__addText__('3. | <name> ~~~ <score>', 29, 280, (80, 80, 1), 24, True, 'Player3score')
    WELCOMEMENU.__addText__('4. | <name> ~~~ <score>', 29, 320, (50, 50, 121), 24, True, 'Player4score')
    WELCOMEMENU.__addText__('---------------------------', 31, 370, (200, 200, 210), 30, True)
    WELCOMEMENU.__addText__('<rank> | You ~~~ <score>', 29, 400, (100, 200, 121), 24, True, 'Myscore')

    WELCOMEMENU.__addInput__('<yourname>', 637, 130, 200, 40, (200, 200, 200), (0, 0, 0), 20)
   


shade = lambda v: [620+v, 0+v, 280-v*2, 270-v*2, (int(5+v/5), int(8+v/5), int(15+v/5)), False, None, (0, 0)]
shadered = lambda v: [620+v, 0+v, 280-v*2, 270-v*2, (int(35+v/5), int(8+v/5), int(15+v/5)), False, None, (0, 0)]
shadegreen = lambda v: [620+v, 0+v, 280-v*2, 270-v*2, (int(0+v/5), int(14+v/5), int(3+v/5)), False, None, (0, 0)]

INGAMEMENU_OBJS =  [shade(i) for i in range(0, 60)] + \
                   [[0, 540, 1000, 60, (15, 7, 2), False, None, (0, 0)]] + \
                   [[10, 0, 880, 10, (0, 0, 0), False, None, (0, 0)]] + \
                   [[0, 0, 10, 590, (0, 0, 0), False, None, (0, 0)]] + \
                   [[890, 0, 10, 590, (0, 0, 0), False, None, (0, 0)]] + \
                   [[0, 590, 900, 10, (0, 0, 0), False, None, (0, 0)]] + \
                   [[298, -10, 4, 80, (40, 40, 0), False, None, (0, 0)]]+\
                   [[76, 70, 448, 5, (70, 70, 0), False, None, (0, 0)]]+\
                   [[290, 70, 20, 30, (70, 0, 0), False, None, (1, 0), (200, 10), 'cursorExtension']]+\
                   [[285, 60, 30, 30, (100, 0, 0), False, None, (1, 0), (200, 10), 'cursor']]+\
                   [[20+(440/7)*8-2, 100, 4, 400, (50, 20, 20), False, None, (0, 0)]] + \
                   [[76, 100, 4, 400, (50, 20, 20), False, None, (0, 0)]] + \
                   [[76, 500, 448, 40, (50, 60, 10), False, None, (0, 0)]] + \
                   [[80 + (440/7)*i-2, 100, 4, 400, (30, 30, 30), False, None, (0, 0)] for i in range(1, 7)] + \
                   [[80, 100 + (400/6)*i-2, 440, 4, (30, 30, 30), False, None, (0, 0)] for i in range(1, 6)] + \
                   [[680, 40, 150, 150, (0, 0, 0), False, os.path.join(script_dir, "..", "images", "moon.png"), (0, 0)]] +\
                   [[560, 360, 300, 180, (43, 10, 1), False, None, (0, 0)]] + \
                   [[570, 370, 10, 10, (191, 105, 19), False, None, (0, 0)]] + \
                   [[570, 520, 10, 10, (191, 105, 19), False, None, (0, 0)]] + \
                   [[840, 520, 10, 10, (191, 105, 19), False, None, (0, 0)]] + \
                   [[840, 370, 10, 10, (191, 105, 19), False, None, (0, 0)]] + \
                   [[560, 360, 300, 180, (25, 10, 6), False, None, (0, 0), (0, 0), 'border']] + \
                   [[10, 10, 80, 30, (10, 10, 107), 'Btnexit', None, (0, 0)]] #EXIT BUTTON 

def reinitIngame():
    global INGAMEMENU
    INGAMEMENU = Menu('INGAME', (5, 8, 15))
    for obj in INGAMEMENU_OBJS:
        INGAMEMENU.__addObject__({"x":obj[0], "y":obj[1],
                               "w":obj[2], "h":obj[3],
                               "c":obj[4], "t":obj[6],
                               "vecxy":obj[7], "lim":obj[-1] if len(obj) == 9 else obj[-2] if len(obj) == 10 else None,
                               "name":obj[-1] if len(obj) == 10 else None}, 
                               clickable=obj[5])
    INGAMEMENU.__addText__('EXIT', 30, 18, 'red', 20)
    INGAMEMENU.__addText__("Rouge: Joueur 1", 600, 400, (164, 40, 12), 20)
    INGAMEMENU.__addText__("Violet: Joueur 2", 600, 430, (40, 27, 56), 20)
    INGAMEMENU.__addText__("C'est au joueur ... de jouer !", 600, 470, (156, 110, 65), 20, True, 'Prompt')
    INGAMEMENU.__addText__("Victoire du joueur ... !", 600, 470, 'green', 20, False, "Victory")



GAMECHOICEMENU_OBJS = [[10, 0, 880, 10, (0, 0, 0), False, None, (0, 0)],
                    [0, 0, 10, 590, (0, 0, 0), False, None, (0, 0)],
                    [890, 0, 10, 590, (0, 0, 0), False, None, (0, 0)],
                    [0, 590, 900, 10, (0, 0, 0), False, None, (0, 0)],
                    [316, 380, 287, 102, (0, 0, 0), 'Btnpvp', None, (0, 0)],
                    [316, 155, 291, 103, (0, 0, 0), 'Btnpve', None, (0, 0)],
                    [316, 266, 291, 106, (0, 0, 0), 'Btnmainlobby', None, (0, 0)],
                    [40, 36, 83, 79, (0, 0, 0), 'Btnbfgc', None, (0, 0)],
                    [50, 240, 200, 300, (0, 0, 0), False, os.path.join(script_dir, "..", "images", "rat-dance.png"), (0, 0)],
                    [465, -10, 300, 300, (0, 0, 0), False, os.path.join(script_dir, "..", "images", "hat.png"), (0, 0)],
                    ]


def reinitGameChoice():
    global GAMECHOICEMENU
    GAMECHOICEMENU = Menu('GAMECHOICE', (10, 10, 10), os.path.join(script_dir, "..", "images", "p4", "Menus", "mGameModes.png"), song=os.path.join(script_dir, "..", "sounds", "home.mp3"))
    for obj in GAMECHOICEMENU_OBJS:
        GAMECHOICEMENU.__addObject__({"x":obj[0], "y":obj[1],
                               "w":obj[2], "h":obj[3],
                               "c":obj[4], "t":obj[6],
                               "vecxy":obj[7], 
                               "lim":obj[-1] if len(obj) == 9 else obj[-2] if len(obj) == 10 else None,
                               "name":obj[-1] if len(obj) == 10 else None}, 
                               clickable=obj[5])
    
    GAMECHOICEMENU.__addText__('Requires internet connection ~~~', 100, 185, (20, 20, 20), 20)
    GAMECHOICEMENU.__addText__('~~~ Requires internet connection.', 610, 315, (20, 20, 20), 20)

PVEMENU_OBJS = [shadered(i) for i in range(0, 60)] + \
                   [[0, 540, 1000, 60, (15, 7, 2), False, None, (0, 0)]] + \
                   [[10, 0, 880, 10, (0, 0, 0), False, None, (0, 0)]] + \
                   [[0, 0, 10, 590, (0, 0, 0), False, None, (0, 0)]] + \
                   [[890, 0, 10, 590, (0, 0, 0), False, None, (0, 0)]] + \
                   [[0, 590, 900, 10, (0, 0, 0), False, None, (0, 0)]] + \
                   [[298, -10, 4, 80, (40, 40, 0), False, None, (0, 0)]]+\
                   [[76, 70, 448, 5, (70, 70, 0), False, None, (0, 0)]]+\
                   [[290, 70, 20, 30, (70, 0, 0), False, None, (1, 0), (200, 10), 'cursorExtension']]+\
                   [[285, 60, 30, 30, (100, 0, 0), False, None, (1, 0), (200, 10), 'cursor']]+\
                   [[20+(440/7)*8-2, 100, 4, 400, (50, 20, 20), False, None, (0, 0)]] + \
                   [[76, 100, 4, 400, (50, 20, 20), False, None, (0, 0)]] + \
                   [[76, 500, 448, 40, (50, 60, 10), False, None, (0, 0)]] + \
                   [[80 + (440/7)*i-2, 100, 4, 400, (30, 30, 30), False, None, (0, 0)] for i in range(1, 7)] + \
                   [[80, 100 + (400/6)*i-2, 440, 4, (30, 30, 30), False, None, (0, 0)] for i in range(1, 6)] + \
                   [[680, 40, 150, 150, (0, 0, 0), False, os.path.join(script_dir, "..", "images", "moon.png"), (0, 0)]] +\
                   [[560, 360, 300, 180, (43, 10, 1), False, None, (0, 0)]] + \
                   [[570, 370, 10, 10, (191, 105, 19), False, None, (0, 0)]] + \
                   [[570, 520, 10, 10, (191, 105, 19), False, None, (0, 0)]] + \
                   [[840, 520, 10, 10, (191, 105, 19), False, None, (0, 0)]] + \
                   [[840, 370, 10, 10, (191, 105, 19), False, None, (0, 0)]] + \
                   [[560, 360, 300, 180, (25, 10, 6), False, None, (0, 0), (0, 0), 'border']] + \
                   [[10, 10, 80, 30, (10, 10, 107), 'Btnexit', None, (0, 0)]] #EXIT BUTTON 

def reinitPVE():
    global PVEMENU
    PVEMENU = Menu('PVE', (35, 8, 15))
    for obj in PVEMENU_OBJS:
        PVEMENU.__addObject__({"x":obj[0], "y":obj[1],
                               "w":obj[2], "h":obj[3],
                               "c":obj[4], "t":obj[6],
                               "vecxy":obj[7], "lim":obj[-1] if len(obj) == 9 else obj[-2] if len(obj) == 10 else None,
                               "name":obj[-1] if len(obj) == 10 else None}, 
                               clickable=obj[5])
    PVEMENU.__addText__('EXIT', 30, 18, 'red', 20)
    PVEMENU.__addText__("Rouge: Joueur", 600, 400, (164, 40, 12), 20)
    PVEMENU.__addText__("Violet: Engine", 600, 430, (40, 27, 56), 20)
    PVEMENU.__addText__("C'est au joueur ... de jouer !", 600, 470, (156, 110, 65), 20, True, 'Prompt')
    PVEMENU.__addText__("Victoire du joueur ... !", 600, 470, 'green', 20, False, "Victory")


ONLINEMENU_OBJS =  [shadegreen(i) for i in range(0, 60)] + \
                   [[0, 540, 1000, 60, (15, 7, 2), False, None, (0, 0)]] + \
                   [[10, 0, 880, 10, (0, 0, 0), False, None, (0, 0)]] + \
                   [[0, 0, 10, 590, (0, 0, 0), False, None, (0, 0)]] + \
                   [[890, 0, 10, 590, (0, 0, 0), False, None, (0, 0)]] + \
                   [[0, 590, 900, 10, (0, 0, 0), False, None, (0, 0)]] + \
                   [[298, -10, 4, 80, (40, 40, 0), False, None, (0, 0)]]+\
                   [[76, 70, 448, 5, (70, 70, 0), False, None, (0, 0)]]+\
                   [[290, 70, 20, 30, (70, 0, 0), False, None, (1, 0), (200, 10), 'cursorExtension']]+\
                   [[285, 60, 30, 30, (100, 0, 0), False, None, (1, 0), (200, 10), 'cursor']]+\
                   [[20+(440/7)*8-2, 100, 4, 400, (50, 20, 20), False, None, (0, 0)]] + \
                   [[76, 100, 4, 400, (50, 20, 20), False, None, (0, 0)]] + \
                   [[76, 500, 448, 40, (50, 60, 10), False, None, (0, 0)]] + \
                   [[80 + (440/7)*i-2, 100, 4, 400, (30, 30, 30), False, None, (0, 0)] for i in range(1, 7)] + \
                   [[80, 100 + (400/6)*i-2, 440, 4, (30, 30, 30), False, None, (0, 0)] for i in range(1, 6)] + \
                   [[680, 40, 150, 150, (0, 0, 0), False, os.path.join(script_dir, "..", "images", "moon.png"), (0, 0)]] +\
                   [[560, 360, 300, 180, (43, 10, 1), False, None, (0, 0)]] + \
                   [[570, 370, 10, 10, (191, 105, 19), False, None, (0, 0)]] + \
                   [[570, 520, 10, 10, (191, 105, 19), False, None, (0, 0)]] + \
                   [[840, 520, 10, 10, (191, 105, 19), False, None, (0, 0)]] + \
                   [[840, 370, 10, 10, (191, 105, 19), False, None, (0, 0)]] + \
                   [[560, 360, 300, 180, (25, 10, 6), False, None, (0, 0), (0, 0), 'border']] + \
                   [[10, 10, 80, 30, (10, 10, 107), 'Btnexit', None, (0, 0)]] #EXIT BUTTON 

def reinitONLINE():
    global ONLINEMENU
    ONLINEMENU = Menu('ONLINE', (0, 14, 3))
    for obj in ONLINEMENU_OBJS:
        ONLINEMENU.__addObject__({"x":obj[0], "y":obj[1],
                               "w":obj[2], "h":obj[3],
                               "c":obj[4], "t":obj[6],
                               "vecxy":obj[7], "lim":obj[-1] if len(obj) == 9 else obj[-2] if len(obj) == 10 else None,
                               "name":obj[-1] if len(obj) == 10 else None}, 
                               clickable=obj[5])
    ONLINEMENU.__addText__('EXIT', 30, 18, 'red', 20)
    ONLINEMENU.__addText__("Rouge: Vous", 600, 400, (164, 40, 12), 20)
    ONLINEMENU.__addText__("Violet: Adversaire", 600, 430, (40, 27, 56), 20)
    ONLINEMENU.__addText__("C'est au joueur ... de jouer !", 600, 470, (156, 110, 65), 20, True, 'Prompt')
    ONLINEMENU.__addText__("Victoire du joueur ... !", 600, 470, 'green', 20, False, "Victory")





MAINLOBBYMENU_OBJS = [[10, 0, 880, 10, (0, 0, 0), False, None, (0, 0)],
                    [0, 0, 10, 590, (0, 0, 0), False, None, (0, 0)],
                    [890, 0, 10, 590, (0, 0, 0), False, None, (0, 0)],
                    [0, 590, 900, 10, (0, 0, 0), False, None, (0, 0)],
                    # make this button tell the server to put us back online not in main lobby [10, 10, 80, 30, (10, 10, 107), 'Btnexit', None, (0, 0)], 
                    [200, 150, 500, 400, (10, 10, 10), False, None, (0, 0)]
                    ]


def reinitMainLobby():
    global MAINLOBBYMENU
    MAINLOBBYMENU = Menu('MAINLOBBY', (10, 20, 10))
    for obj in MAINLOBBYMENU_OBJS:
        MAINLOBBYMENU.__addObject__({"x":obj[0], "y":obj[1],
                               "w":obj[2], "h":obj[3],
                               "c":obj[4], "t":obj[6],
                               "vecxy":obj[7], 
                               "lim":obj[-1] if len(obj) == 9 else obj[-2] if len(obj) == 10 else None,
                               "name":obj[-1] if len(obj) == 10 else None}, 
                               clickable=obj[5])
    
    MAINLOBBYMENU.__addText__('MAIN ~ LOBBY', 332, 60, (100, 80, 200), 50)
    MAINLOBBYMENU.__addText__('Players online', 398, 170, (100, 100, 100), 20)
    MAINLOBBYMENU.__addText__('--------------------------------------------', 358, 186, (100, 100, 100), 20)
    MAINLOBBYMENU.__addText__('Main Lobby Players', 445, 205, (16, 201, 85), 18, name='mainlobbyplayers', center=True)
    MAINLOBBYMENU.__addText__('EXIT', 30, 18, 'red', 20)
    






def REINIT_ALL_DATA():
    reinitGameChoice()
    reinitMainLobby()
    reinitONLINE()
    reinitPVE()
    reinitIngame()
    reinitWelcome()
    

REINIT_ALL_DATA()

ALL_MENUS = [WELCOMEMENU, INGAMEMENU, GAMECHOICEMENU, PVEMENU, ONLINEMENU, MAINLOBBYMENU]