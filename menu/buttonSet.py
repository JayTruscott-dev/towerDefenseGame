import os
import pygame

pygame.init()
os.environ['SDL_VIDEO_CENTERED'] = '1'
screen = pygame.display.set_mode((615,800))

spritesheet = pygame.image.load("menu_buttons.png")
        
class SpriteSheet:
    def __init__(self):
        self.sheet = spritesheet
        
    def image_at(self, rectangle):
        # rectangle = x, y, x+offset, y+offset
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0,0), rect)
        
        return image
    
    
class Sprite:
    def __init__(self):
        self.image = None
        self.name = ''
        self.screen = screen
    
    def blitter(self):
        self.rect = self.image.get_rect()
        self.rect.topleft = self.x, self.y
        self.screen.blit(self.image, self.rect)
        

class ButtonSet:
    def __init__(self):
        self.pieces = []
        self._load_pieces()
    
    def _load_pieces(self):
        ss = SpriteSheet()
        up_sell_rect = (151, 42, 304, 116)
        menu_bg = ss.image_at(up_sell_rect)
        self.pieces.append(menu_bg)
        up_rect = (183, 124, 257, 197)
        menu_up_bg = ss.image_at(up_rect)
        self.pieces.append(menu_up_bg)
        
        sell_rect = (183, 124, 257, 197)
        menu_sell_bg = ss.image_at(sell_rect)
        self.pieces.append(menu_sell_bg)
        

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    #screen.blit()
    
    pygame.display.update()

pygame.quit()