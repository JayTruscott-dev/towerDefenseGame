import pygame
import math
import os

from .tower import Tower
from menu.menu import Menu

ui_path = "media/UserInterface"
menu_bg = pygame.image.load(os.path.join(ui_path, "menu_bg.png"))
upgrade_btn = pygame.transform.scale(pygame.image.load(os.path.join(ui_path, "upgrade_icon.png")), (35,35))
sell_btn = pygame.transform.scale(pygame.image.load(os.path.join(ui_path, "sell_icon.png")), (35,35))

imgs = []
for i in range(1,4,1):
    imgs.append(pygame.transform.scale(pygame.image.load(os.path.join("media/Towers/3-CannonTower", "Cannon-" + str(i) + ".png")), (55,110)))
        
class Cannon(Tower):
    def __init__(self, x, y):
        # PARENT CLASS
        super().__init__(x,y)
        
        # TOWER SIZING AND IMAGES
        self.imgs = imgs[:]
        self.width = 55
        self.height = 110
        
        # TOWER POSITIONING
        self.left_coord = self.x - (self.width/2)
        self.top_coord = self.y
        self.right = False
        self.up = True
        
        # TOWER RANGE
        self.RNG = 125
        self.original_range = self.RNG
        self.inRange = False
        
        # TOWER DAMAGE
        self.DMG = 3*self.level
        self.original_damage = self.DMG
        
        # ATTACKING
        self.speed = 2500
        self.clock = pygame.time.Clock()
        self.cooldown_tracker = 0
        self.hit_enemy = False
        
        # PROJECTILES
        self.arrow_imgs = []
        self.arrow_imgs.append(pygame.image.load(os.path.join("media/Towers/misc", "cannon.png")))
        self.move_x = 10
        self.move_y = 10
        self.arrowX = self.x - (self.width/2)
        self.arrowY = self.y
        
        # BUYING AND MOVING
        self.moving = False
        self.name = "cannon"
        self.price = [1000,1250,1500]
        
        # MENU
        self.menu = Menu(self, self.x, self.y, menu_bg, [1250, 1500, "MAX"])
        self.menu.add_btn(upgrade_btn, "Upgrade")
        self.menu.add_btn(sell_btn, "Sell")
    
    def draw(self, screen):
        """ Accesses the draw method from the Tower superclass.
            Params: screen (Surface): The pygame surface used for blitting
            Return: None
        """
        # Draw grey range circle, translucent, centered around the tower
        circle_surface = pygame.Surface((self.RNG*4, self.RNG*4), pygame.SRCALPHA, 32)
        
        pygame.draw.circle(circle_surface, (100,100,100,50), (self.RNG, self.RNG), self.RNG, 0)
        screen.blit(circle_surface, (self.x-self.RNG, self.y-self.RNG))
        
        super().draw(screen, self.imgs)
        
        # Map blitting of each arrow towards left/right enemies
        if self.inRange and not(self.hit_enemy):
            arrow_img = self.arrow_imgs[0]
            arrow_img = pygame.transform.flip(arrow_img, self.right, self.up)
            
            screen.blit(arrow_img, (self.x, self.y))
    
    def change_range(self, r):
        """ Changes the range of the cannon tower
            Params: r (int): new RNG of the tower
            Return: None
        """
        self.RNG = r
        
    def change_damage(self, d):
        """ Changes the damage of the cannon tower
            Params: d (int): new DMG for the cannon tower
            Return: None
        """
        self.DMG = d

    def update_projectile(self):
        """ Updates the projectile starting position to the tower's placement location
            Params: None
            Return: None
        """
        self.left_coord = self.x - self.width/2
        self.top_coord = self.y
        self.arrowX = self.left_coord
        self.arrowY = self.top_coord
        
    def attack(self, enemies):
        """ Defines tower attacks against enemies in the enemy list, modifies that list.
            Params: enemies (list): list of current wave enemies
            Return: coins (int): number of coins earned when the enemy dies
        """
        coins = 0
        self.inRange = False
        enemyClosest = []
        for enemy in enemies:
            X = enemy.x
            Y = enemy.y
            
            dis = math.sqrt((self.x -X)**2 + (self.y - Y)**2)
            if dis <= self.RNG:
                self.inRange = True
                enemyClosest.append(enemy)
                
        self.hit_enemy = False
        enemyClosest.sort(key=lambda x: x.x)
        enemyClosest.reverse()
        
        if len(enemyClosest) > 0 and self.cooldown_tracker >= self.speed:
            first_enemy = enemyClosest[0]
            e_width = first_enemy.width
            e_height = first_enemy.height
            e_x = first_enemy.x
            e_y = first_enemy.y
            
            arrow_dirn = (e_x - self.arrowX, e_y - self.arrowY)
            
            if e_x > self.arrowX: # Enemy right of Tower
                arrow_dirn = (arrow_dirn[0] + e_width, arrow_dirn[1])
                
            if e_y > self.arrowY: # Enemy below Tower
                arrow_dirn = (arrow_dirn[0], arrow_dirn[1] + e_height)
            dis_to_enemy = math.sqrt((arrow_dirn[0]**2 + arrow_dirn[1]**2))
            dis_speed = dis_to_enemy / 25
            
            arrow_dirn = (arrow_dirn[0]/dis_speed, arrow_dirn[1]/dis_speed)
            
            if arrow_dirn[0] <= 0:
                self.right = False
            else:
                self.right = True
            if arrow_dirn[1] <= 0:
                self.up = True
            else:
                self.up = False
            
            self.move_x, self.move_y = ((self.arrowX + arrow_dirn[0]), (self.arrowY + arrow_dirn[1]))
            
            self.arrowX = self.move_x
            self.arrowY = self.move_y
            
            self.hit_enemy = first_enemy.collide(self.arrowX, self.arrowY)
            
            if self.hit_enemy:
                if first_enemy.died(self.DMG):
                    first_enemy.has_died = True
                    coins += first_enemy.coins
                
                self.cooldown_tracker = 0
                self.arrowX = self.left_coord
                self.arrowY = self.top_coord
                self.right = False
                self.up = False
                
        return coins