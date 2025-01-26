from gameimports import *
pygame.init()


class Main:
    def __init__(self, wnw, wnh):
        self.wnw = wnw
        self.wnh = wnh
        self.window = pygame.display.set_mode((wnw, wnh))
        self.running = True
        self.location = 'WELCOME'
        self.fps = 60
        self.clock = pygame.time.Clock()

    
    def __drawElems__(self, elems):
        for elem in elems:
            attr = elem['attributes']
            color = elem['color']
            if elem['texture'] is None:
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
            

   



    def __render__(self, menu):
        pygame.display.flip()
        menu_data = menu.__getInfo__()
        self.window.fill(menu_data['Bg'])
        pygame.display.set_caption(f'PROJECT GALAXY MADNESS - {menu_data['Name']}')
        self.__drawElems__(menu_data['Elements'])
        self.clock.tick(self.fps)

    def __listenToEvents__(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.location = 'INGAME'





if __name__ == "__main__":
    GameInstance = Main(900, 600)
    while GameInstance.running:
        GameInstance.__render__(next((menu for menu in ALL_MENUS if menu.__getInfo__()['Name'] == GameInstance.location), None))
        GameInstance.__listenToEvents__()