import pygame

class Menu:
    def __init__(self, name, bg):
        self.name = name
        self.bg = bg
        self.all_objects = []
    def __addObject__(self, data, clickable=False):
        """Excpects a data list with req|: x, y, w, h, c, vecxy, lim. 
           w -> width;
           h -> height;
           c -> color;
           t -> Texture, None if no texture, or link to the image;
           vecxy -> Tuple, Vector of movement.
           lim -> Corresponds to a range of movement.
           Renders a 2D menu UI object that can be clickable.
        """

        self.all_objects.append({"ogX":data['x'], "ogY":data['y'],"attributes":pygame.Rect(data["x"], data["y"], data["w"], data["h"]), "color":data["c"], "texture":data["t"], "name":data["name"], "vector": [data["vecxy"][0], data["vecxy"][1]], "limit":data["lim"],"clickable":clickable})

    def __getInfo__(self):
        return {'Id':id(self),'Name':self.name, 'Bg':self.bg, 'Elements':self.all_objects}
    
        