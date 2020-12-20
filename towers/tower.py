import pygame
import os
import math

from menu.menu import Menu

ui_path = "media/UserInterface"
menu_bg = pygame.image.load(os.path.join(ui_path, "menu_bg.png"))
upgrade_btn = pygame.transform.scale(pygame.image.load(os.path.join(ui_path, "upgrade_icon.png")), (35,35))
sell_btn = pygame.transform.scale(pygame.image.load(os.path.join(ui_path, "sell_icon.png")), (35,35))

class Tower:
    # This is the Tower abstract class
    def __init__(self,x,y):
        """ Initializes a Tower with the following attributes.
            Params: x (int): Width of the Tower
                    y (int): Height of the Tower
            Return: N/A
        """
        # IMAGES & POSITIONING
        self.imgs = []
        self.x = x
        self.y = y
        self.centeringWidth = 50
        self.centeringHeight = 50
        
        # MENU
        self.menu = Menu(self, self.x, self.y, menu_bg, [2000, 2200, "MAX"])
        
        # SELLING
        self.sell_price = [0,0,0]
        self.price = [0,0,0]
        self.sold = False
        
        # PLACEMENT
        self.selected = False
        self.place_color = (0,0,255,100)
        
        # RANGE
        self.RNG = 150
        self.range_buff = 0
        
        # DAMAGE
        self.DMG = 1
        self.damage_buff = 0
        
        # LEVEL
        self.level = 1
    
    def sell(self):
        """ 
        """
        return self
    
    def get_sell_price(self):
        
        self.sold = True
        price = self.price[self.level - 1] / 2
        return int(price)

    def upgrade(self):
        """ 
        Defines Tower attributes that change on upgrading the tower
        Params: None
        Return: None
        """
        self.level += 1
    
    # Returns upgrade_cost, if it's 0 then can't upgrade further
    def get_upgrade_cost(self):
        """
        """
        upgrade_cost = self.price[0]
        if self.level < len(self.imgs):
            upgrade_cost = self.price[self.level - 1]
        else:
            upgrade_cost = "MAX"
        return upgrade_cost
    
    # Function handles drawing the Tower to the screen at the interaction point (x,y)
    def draw(self, screen, t_img):
        """ Handles drawing of the Tower to the screen at the interaction point (x,y).
            Params: screen (Surface): The pygame surface used for blitting
            Return: None
        """
        # Draws Tower image to the screen
        img = t_img[self.level - 1]
        #centeringWidth = img.get_width()/2
        #centeringHeight = img.get_height()/2
        screen.blit(img, (self.x-(self.width/2), self.y-(self.height/2)))
        
        # Draws Tower menu to the screen
        if self.selected:
            self.menu.draw(screen)
    
    def draw_radius(self, screen):
        if self.selected: # Draws range circle for the selected tower
            surf = pygame.Surface((self.RNG*4, self.RNG*4), pygame.SRCALPHA, 32)
            pygame.draw.circle(surf, (100,100,100,50), (self.RNG, self.RNG), self.RNG, 0)
            
            screen.blit(surf, (self.x-(self.RNG), self.y-(self.RNG)))
            
    def draw_placement(self, screen):
        # First draws range circle of tower
        surf = pygame.Surface((self.RNG*4, self.RNG*4), pygame.SRCALPHA, 32)
        pygame.draw.circle(surf, self.place_color, (50,50), 50, 0)
        
        screen.blit(surf, (self.x-50, self.y-50))
        
    # Function handles user interaction with the Tower
    def click(self, X, Y):
        """ Handles user interaction with a Tower. Returns true if the user clicks on a Tower.
            Params: X (int): The x coord of the user click
                    Y (int): The y coord of the user click
            Return: Bool
        """
        img = self.imgs[self.level-1]
        t_width = img.get_width()//2
        t_height = img.get_height()//2
        if X <= self.x - t_width + self.width and X >= self.x - t_width:
            if Y <= self.y + self.height - t_height and Y >= self.y - t_height:
                return True
        return False

    def move(self, x, y):
        """
        """
        self.x = x
        self.y = y
        
        self.menu.x = x
        self.menu.y = y
        self.menu.update()
        self.update_projectile()
        
    def collide(self, otherTower):
        hasCollided = True
        x2 = otherTower.x
        y2 = otherTower.y
        
        dis = math.sqrt((x2 - self.x)**2 + (y2 - self.y)**2)
        
        if dis >= 100:
            hasCollided = False
        
        return hasCollided
    
    def collideRNG(self, otherTower):
        """
        This method checks if the current tower's RNG circle collides with another tower.
        Params: otherTower (Object): Tower object from a list
        Return: Boolean: True if the other tower is within range of the current tower
        """
        tower_in_range = False
        x2 = otherTower.x
        y2 = otherTower.y
        
        reach = self.RNG
        
        dis = math.sqrt((x2 - self.x)**2 + (y2 - self.y)**2)
        
        if dis <= reach:
            tower_in_range = True
        
        return tower_in_range
