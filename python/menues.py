import pygame
pygame.init()

class Menu:
    def __init__(self, name, bg, image=None):
        self.name = name
        self.bg = bg
        self.all_objects = []
        self.all_texts = []
        self.image = image

    def __addObject__(self, data, clickable=False,  dontdisplay=False):
        """Excpects a data list with req|: x, y, w, h, c, vecxy, lim. 
           w -> width;
           h -> height;
           c -> color;
           t -> Texture, None if no texture, or link to the image;
           vecxy -> Tuple, Vector of movement.
           lim -> Corresponds to a range of movement.
           Clickable excpects either False for not a button, or a function name for a button when it is clicked.
           Renders a 2D menu UI object that can be clickable.

        """
        self.all_objects.append({"ogX":data['x'], "ogY":data['y'],"attributes":pygame.Rect(data["x"], data["y"], data["w"], data["h"]), "color":data["c"], "texture":data["t"], "name":data["name"], "vector": [data["vecxy"][0], data["vecxy"][1]], "limit":data["lim"],"clickable":clickable, "dontdisplay":dontdisplay})

    def __addText__(self, string:str, x:int, y:int, color:tuple, size:int, display:bool=True, name:str=None):
        """Displays a text at a position with a color at a certain size."""
        self.all_texts.append({"string":string, "x":x, "y":y, "color":color, "size":size, "display":display, "name":name})

    def __getInfo__(self):
        return {'Id':id(self),'Name':self.name, 'Bg':self.bg, 'Img':self.image, 'Elements':self.all_objects, 'Texts':self.all_texts}
        
    def __setInfo__(self, cat, data):
        if cat not in ('Name', 'Bg', 'Elements', 'Texts'):
            print('Not Valid category')
            return
        if cat == "Texts":
            self.all_texts = data
        