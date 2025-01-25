from menues import Menu

WELCOMEMENU = Menu('WELCOME', (10, 10, 10))
WELCOMEMENU_OBJS = [[10, 10, 10, 10, 'red', False]]
for obj in WELCOMEMENU_OBJS:
    WELCOMEMENU.__addObject__({"x":obj[0], "y":obj[1],
                               "w":obj[2], "h":obj[3],
                               "c":obj[4]}, clickable=obj[5])