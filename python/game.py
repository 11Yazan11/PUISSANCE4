import pygame
from data import *


class Game:
    def __init__(self, main):
        self.main = main

    def __handle_event__(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if 80 < event.pos[0] < 520 and 100 < event.pos[1] < 500 and self.main.location == "INGAME":
                elements = INGAMEMENU.__getInfo__()['Elements']
                cursor = next((element for element in elements if element['name'] == 'cursor'), None)
                cursorExt = next((element for element in elements if element['name'] == 'cursorExtension'), None)
                cursorP = cursor['attributes']
                cursorExtP = cursorExt['attributes']
                caseWidth = 442/7
                cursorP.x = ((min(max(event.pos[0]-15, 120), 484)//caseWidth)*caseWidth)+32
                cursorExtP.x = cursorP.x + 5
                cursorOgVector = cursor['vector']
                cursorExtOgVector = cursor['vector']
                cursor['vector'] = [0,0]
                cursorExt['vector'] = [0,0]


        



