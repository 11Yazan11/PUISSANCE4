from menues import Menu
import os



script_dir = os.path.dirname(__file__)


WELCOMEMENU_OBJS = [[10, 0, 880, 10, (0, 0, 0), False, None, (0, 0)],
                    [0, 0, 10, 590, (0, 0, 0), False, None, (0, 0)],
                    [890, 0, 10, 590, (0, 0, 0), False, None, (0, 0)],
                    [0, 590, 900, 10, (0, 0, 0), False, None, (0, 0)],
                    [310, 358, 287, 103, (100, 0, 0), 'Btnplay', None, (0, 0), True] # add the other buttons
                    ]
def reinitWelcome():
    global WELCOMEMENU
    WELCOMEMENU = Menu('WELCOME', (10, 10, 10), os.path.join(script_dir, "..", "images", "p4", "Menus", "mBase.png"))
    for obj in WELCOMEMENU_OBJS:
        WELCOMEMENU.__addObject__({"x":obj[0], "y":obj[1],
                               "w":obj[2], "h":obj[3],
                               "c":obj[4], "t":obj[6],
                               "vecxy":obj[7], "lim":obj[-1] if len(obj) == 9 else obj[-2] if len(obj) == 10 else None,
                               "name":obj[-1] if len(obj) == 10 else None}, 
                               clickable=obj[5])


shade = lambda v: [620+v, 0+v, 280-v*2, 270-v*2, (int(5+v/5), int(8+v/5), int(15+v/5)), False, None, (0, 0)]
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
        INGAMEMENU.__addText__("Beige: Joueur 1", 600, 400, (82, 71, 64), 20)
        INGAMEMENU.__addText__("Violet: Joueur 2", 600, 430, (40, 27, 56), 20)
        INGAMEMENU.__addText__("C'est au joueur ... de jouer !", 600, 470, (156, 110, 65), 20, True, 'Prompt')
        INGAMEMENU.__addText__("Victoire du joueur ... !", 600, 470, 'green', 20, False, "Victory")



GAMECHOICEMENU_OBJS = [[10, 0, 880, 10, (0, 0, 0), False, None, (0, 0)],
                    [0, 0, 10, 590, (0, 0, 0), False, None, (0, 0)],
                    [890, 0, 10, 590, (0, 0, 0), False, None, (0, 0)],
                    [0, 590, 900, 10, (0, 0, 0), False, None, (0, 0)],
                    [316, 380, 287, 102, (100, 0, 0), 'Btnpvp', None, (0, 0)],
                    ]


def reinitGameChoice():
    global GAMECHOICEMENU
    GAMECHOICEMENU = Menu('GAMECHOICE', (10, 10, 10), os.path.join(script_dir, "..", "images", "p4", "Menus", "mGameModes.png"))
    for obj in GAMECHOICEMENU_OBJS:
        GAMECHOICEMENU.__addObject__({"x":obj[0], "y":obj[1],
                               "w":obj[2], "h":obj[3],
                               "c":obj[4], "t":obj[6],
                               "vecxy":obj[7], "lim":obj[-1] if len(obj) == 9 else obj[-2] if len(obj) == 10 else None,
                               "name":obj[-1] if len(obj) == 10 else None}, 
                               clickable=obj[5])



def REINIT_ALL_DATA():
    reinitGameChoice()
    reinitIngame()
    reinitWelcome()

REINIT_ALL_DATA()

ALL_MENUS = [WELCOMEMENU, INGAMEMENU, GAMECHOICEMENU]