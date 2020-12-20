import pygame
import math
import os
import time

from .tower import Tower
from menu.menu import Menu

ui_path = "media/UserInterface"
menu_bg = pygame.image.load(os.path.join(ui_path, "menu_bg.png"))
upgrade_btn = pygame.transform.scale(pygame.image.load(os.path.join(ui_path, "upgrade_icon.png")), (35,35))
sell_btn = pygame.transform.scale(pygame.image.load(os.path.join(ui_path, "sell_icon.png")), (35,35))

ranger_imgs = []
toughen_imgs = []
for i in range(1,4,1):
    ranger_imgs.append(pygame.image.load(os.path.join("media/Towers/4-RangerTower", "Ranger-" + str(i) + ".png")))
    toughen_imgs.append(pygame.image.load(os.path.join("media/Towers/5-ToughenTower", "Toughen-" + str(i) + ".png")))

price = [1750,2000,2200]
effect = [0.2,0.4,0.6]

RNG = 150

class Ranger(Tower):
    def __init__(self, x, y):
        super().__init__(x,y)
        
        # TOWER SIZING AND IMAGES
        self.imgs = ranger_imgs[:]
        self.height = 63
        self.width = 100
        
        # TOWER RANGE
        self.RNG = RNG
        
        # IMPROVEMENTS
        self.speed = 0
        self.effect = effect
        
        # BUYING & MOVING
        self.moving = False
        self.name = "ranger"
        self.price = price
        
        # MENU
        self.menu = Menu(self, self.x, self.y, menu_bg, [1750, 2000, "MAX"])
        self.menu.add_btn(upgrade_btn, "Upgrade")
        self.menu.add_btn(sell_btn, "Sell")
    
    def draw(self, screen):
        circle_surface = pygame.Surface((self.RNG*4, self.RNG *4), pygame.SRCALPHA, 32)
        pygame.draw.circle(circle_surface, (100,100,100,50), (self.RNG, self.RNG), self.RNG, 0)
        
        screen.blit(circle_surface, (self.x-self.RNG, self.y-self.RNG))
            
        super().draw(screen, self.imgs)
        
    def update_projectile(self):
        pass
    
    def improve(self, originalRNG):
        return originalRNG + round(originalRNG * self.effect[self.level-1])
    
class Toughen(Tower):
    def __init__(self, x, y):
        super().__init__(x,y)
        
        # TOWER SIZING AND IMAGES
        self.imgs = toughen_imgs[:]
        self.height = 63
        self.width = 100
        
        # TOWER RANGE
        self.RNG = RNG
        
        # IMPROVEMENTS
        self.speed = 0
        self.effect = effect
        
        # BUYING & MOVING
        self.moving = False
        self.name = "toughen"
        self.price = price
        
        # MENU
        self.menu = Menu(self, self.x, self.y, menu_bg, [1750, 2000, "MAX"])
        self.menu.add_btn(upgrade_btn, "Upgrade")
        self.menu.add_btn(sell_btn, "Sell")
    
    def draw(self, screen):
        circle_surface = pygame.Surface((self.RNG * 4, self.RNG * 4), pygame.SRCALPHA, 32)
        pygame.draw.circle(circle_surface, (100,100,100,50), (self.RNG, self.RNG), self.RNG, 0)
            
        screen.blit(circle_surface, (self.x-self.RNG, self.y-self.RNG))
        super().draw(screen, self.imgs)
        
    def update_projectile(self):
        pass
    
    def improve(self, originalDMG):
        return originalDMG + round(originalDMG * self.effect[self.level-1])