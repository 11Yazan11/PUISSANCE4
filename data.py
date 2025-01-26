from menues import Menu

WELCOMEMENU = Menu('WELCOME', (10, 10, 10))
WELCOMEMENU_OBJS = [[10, 0, 880, 10, (0, 0, 0), False, None, (0, 0)],
                    [0, 0, 10, 590, (0, 0, 0), False, None, (0, 0)],
                    [890, 0, 10, 590, (0, 0, 0), False, None, (0, 0)],
                    [0, 590, 900, 10, (0, 0, 0), False, None, (0, 0)],
                    [400, 250, 100, 100, 'black', True, 'images/play.png', (0, 0)]]
for obj in WELCOMEMENU_OBJS:
    WELCOMEMENU.__addObject__({"x":obj[0], "y":obj[1],
                               "w":obj[2], "h":obj[3],
                               "c":obj[4], "t":obj[6],
                               "vecxy":obj[7], "lim":obj[-1] if len(obj) == 9 else None}, clickable=obj[5])

INGAMEMENU = Menu('INGAME', (5, 8, 15))
shade = lambda v: [620+v, 0+v, 280-v*2, 270-v*2, (int(5+v/5), int(8+v/5), int(15+v/5)), False, None, (0, 0)]
INGAMEMENU_OBJS =  [shade(i) for i in range(0, 60)] + \
                   [[0, 540, 1000, 60, (15, 7, 2), False, None, (0, 0)]] + \
                   [[10, 0, 880, 10, (0, 0, 0), False, None, (0, 0)]] + \
                   [[0, 0, 10, 590, (0, 0, 0), False, None, (0, 0)]] + \
                   [[890, 0, 10, 590, (0, 0, 0), False, None, (0, 0)]] + \
                   [[0, 590, 900, 10, (0, 0, 0), False, None, (0, 0)]] + \
                   [[298, -10, 4, 80, (40, 40, 0), False, None, (0, 0)]]+\
                   [[76, 70, 448, 5, (70, 70, 0), False, None, (0, 0)]]+\
                   [[290, 70, 20, 30, (70, 0, 0), False, None, (1, 0), (200, 10)]]+\
                   [[285, 60, 30, 30, (100, 0, 0), False, None, (1, 0), (200, 10)]]+\
                   [[20+(440/7)*8-2, 100, 4, 400, (50, 20, 20), False, None, (0, 0)]] + \
                   [[76, 100, 4, 400, (50, 20, 20), False, None, (0, 0)]] + \
                   [[76, 500, 448, 40, (50, 60, 10), False, None, (0, 0)]] + \
                   [[80 + (440/7)*i-2, 100, 4, 400, (30, 30, 30), False, None, (0, 0)] for i in range(1, 7)] + \
                   [[80, 100 + (400/6)*i-2, 440, 4, (30, 30, 30), False, None, (0, 0)] for i in range(1, 6)] + \
                   [[680, 40, 150, 150, (0, 0, 0), False, 'images/moon.png', (0, 0)]] 
for obj in INGAMEMENU_OBJS:
    INGAMEMENU.__addObject__({"x":obj[0], "y":obj[1],
                               "w":obj[2], "h":obj[3],
                               "c":obj[4], "t":obj[6],
                               "vecxy":obj[7], "lim":obj[-1] if len(obj) == 9 else None}, clickable=obj[5])
ALL_MENUS = [WELCOMEMENU, INGAMEMENU]