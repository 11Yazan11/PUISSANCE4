import pygame

class Menu:
    def __init__(self, name, bg):
        self.name = name
        self.bg = bg
        self.all_objects = []
    def __addObject__(self, data, clickable=False):
        """Excpects a data list with x, y, w, h, c. 
           w -> width;
           h -> height;
           c -> color;
           Renders a 2D menu UI object that can be clickable.
        """
        self.all_objects.append({"attributes":pygame.Rect(data["x"], data["y"], data["w"], data["h"]), "color":data["c"], "clickable":clickable})
    def __getInfo__(self):
        return {'Id':id(self),'Name':self.name, 'Bg':self.bg, 'Elements':self.all_objects}
    
        