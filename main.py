from gameimports import *
pygame.init()


class Main:
    def __init__(self, wnw, wnh):
        self.wnw = wnw
        self.wnh = wnh
        self.window = pygame.display.set_mode((wnw, wnh))
        self.running = True
    
    def __drawElems__(self, elems):
        for elem in elems:
            attr = elem['attributes']
            color = elem['color']
            pygame.draw.rect(self.window, color, (attr.x, attr.y, attr.w, attr.h))

    def __render__(self, menu):
        pygame.display.flip()
        menu_data = menu.__getInfo__()
        self.window.fill(menu_data['Bg'])
        pygame.display.set_caption(f'PROJECT GALAXY MADNESS - {menu_data['Name']}')
        self.__drawElems__(menu_data['Elements'])

    def __listenToEvents__(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False





if __name__ == "__main__":
    GameInstance = Main(1000, 600)
    while GameInstance.running:
        GameInstance.__render__(WELCOMEMENU)
        GameInstance.__listenToEvents__()