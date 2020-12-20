import pygame
import math
import os

from .tower import Tower

class Burning(Tower):
    def __init__(self, x, y):
        super().__init__(x, y)
        
        # IMAGES
        self.imgs = []
        self.width = 60
        self.height = 90
        for burning_level in range(1,4,1):
            self.imgs.append(pygame.transform.scale(pygame.image.load(os.path.join("media/Towers/4-BurningTower", "Burning-" + str(burning_level) + ".png")), (self.width,self.height)))
        
        # POSITIONING
        self.left_coord = x - self.width/2
        self.top_coord = y - self.width/2
        self.right = False
        self.up = True
        
        # SHOOTING
        self.projectiles = 1
        self.projectile_state = "ready"
        self.move_x = 10
        self.move_y = 10
        self.arrowX = x
        self.arrowY = y
        self.arrow_pos = []
        self.arrow_index = 0
        self.travel_dis = 0
        self.arrow_imgs = [] # Image is loaded with DOWN/LEFT orientation
        self.arrow_imgs.append(pygame.image.load(os.path.join("media/Towers/misc", "fire.png")))
        self.range = 100
        self.inRange = False
        
        # HITTING ENEMIES
        self.DMG = 1
        self.hit_enemy = False
        
        # TIMING
        self.speed = 5 # Defines cooldown time
        self.clock = pygame.time.Clock()
        self.cooldown_tracker = 0

    def draw(self, screen):
        """ Accesses the draw method from the Tower superclass.
            Params: screen (Surface): The pygame surface used for blitting
            Return: None
        """
        
        # Draw grey range circle, translucent, centered around the tower
        circle_surface = pygame.Surface((self.range*4, self.range*4), pygame.SRCALPHA, 32)
        
        pygame.draw.circle(circle_surface, (100,100,100,50), (self.range, self.range), self.range, 0)
        screen.blit(circle_surface, (self.x-self.range, self.y-self.range))
        
        super().draw(screen)
        
        if self.inRange and not(self.hit_enemy): # Map blitting of each arrow towards left/right enemies
            arrow_img = self.arrow_imgs[0]
            #if not(self.left): # If enemy is to the left, blit arrow towards them
            #    pygame.transform.flip(arrow_img, True, False)
            #else:
            #    self.move_x *= -1
            #if self.up:
            #    pygame.transform.flip(arrow_img, False, True)
            #    self.move_y *= -1
            #else:
            #    self.move_y *= 1
            #shooter(self.x, self.y)
            
            #self.arrowX += self.move_x
            #self.arrowY += self.move_y
            arrow_img = pygame.transform.flip(arrow_img, self.right, self.up)
            
            if self.arrowX != self.left_coord + self.width/2 and self.arrowY != self.top_coord:
                screen.blit(arrow_img, (self.arrowX, self.arrowY))
        
        #self.move(
    
    def change_range(self, r):
        """ Changes the range of the archer tower (by level?).
            Params: r (int): Range of the tower
            Return: None
        """
        self.range = r

    def attack(self, enemies):
        """ Defines tower attacks against enemies in the enemy list, modifies that list.
            Params: enemies (list): List of current wave enemies
            Return: None
        """
        #self.cooldown_tracker += self.clock.get_time()
        self.inRange = False
        enemyClosest = []
        for enemy in enemies:
            X = enemy.x
            Y = enemy.y
            
            dis = math.sqrt((self.x - X)**2 + (self.y - Y)**2)
            if dis <= self.range:
                self.inRange = True
                enemyClosest.append(enemy)
                
        self.hit_enemy = False
        enemyClosest.sort(key=lambda x: x.x)
        enemyClosest.reverse() # Should reverse the list, making Tower hit closest enemy (instead of newest enemy inRange)
        if len(enemyClosest) > 0 and self.cooldown_tracker >= self.speed:
            #self.cooldown_tracker = 0
            
            first_enemy = enemyClosest[0]
            e_width = first_enemy.width
            e_height = first_enemy.height
            e_x = first_enemy.x #+ first_enemy.width/2
            e_y = first_enemy.y #+ first_enemy.height/2
            
            #middle_x = (e_x - self.arrowX)/2
            #middle_y = (e_y - self.arrowY)/2
            arrow_dirn = (e_x - self.arrowX, e_y - self.arrowY)
            
            # Attempt to draw flames as big as the distance between Tower and Enemy
            #dirn_x_int = int(arrow_dirn[0])
            #dirn_y_int = int(arrow_dirn[1])
            #if dirn_x_int < 0:
            #    dirn_x_int *= -1
            #if dirn_y_int < 0:
            #    dirn_y_int *= -1
            #self.arrow_imgs[0] = pygame.transform.scale(self.arrow_imgs[0], (dirn_x_int, dirn_y_int))
            
            if e_x > self.arrowX: # Enemy right of Tower
                arrow_dirn = (arrow_dirn[0] + e_width, arrow_dirn[1])
            #else:
            #    arrow_dirn[0] = e_x + e_width - self.arrowX
            if e_y > self.arrowY: # Enemy below Tower
                arrow_dirn = (arrow_dirn[0], arrow_dirn[1] + e_height)
            #else:
            #    arrow_dirn[1] = e_y + e_height - self.arrowY
            #arrow_dirn = ((e_x - self.arrowX), (e_y - self.arrowY))
            dis_to_enemy = math.sqrt((arrow_dirn[0]**2 + arrow_dirn[1]**2))
            dis_speed = dis_to_enemy / 40#dis_to_enemy # Should make fireballs the fastest projectile
            
            arrow_dirn = (arrow_dirn[0]/dis_speed, arrow_dirn[1]/dis_speed)
            
            if arrow_dirn[0] <= 0: # Starting arrow X value is > enemy X value
                self.right = False # AKA - enemy is left of the tower
                # Collide point should be right corner
                # Note: closest corner causes glitches (use far corner)
            else:                  # Starting arrow X value is < enemy X value
                self.right = True  # AKA - enemy is right of the tower
                # Collide point should be left corner
            if arrow_dirn[1] <= 0: # Starting arrow Y value is > enemy Y value
                self.up = True     # AKA - enemy is above the tower
                # Collide point should be bottom corner
            else:                  # Starting arrow Y value is < enemy Y value
                self.up = False    # AKA - enemy is below the tower
                 # Collide point should be top corner
            self.move_x, self.move_y = ((self.arrowX + arrow_dirn[0]), (self.arrowY + arrow_dirn[1]))
            
            self.arrowX = self.move_x
            self.arrowY = self.move_y
            
            
            
            self.hit_enemy = first_enemy.collide(self.arrowX, self.arrowY)
            if self.hit_enemy:
                #self.hasDied = first_enemy.died()
                if first_enemy.died(self.DMG): # Runs died method from Enemy superclass (subtracts DMG from enemy health)
                    first_enemy.has_died = True
                    enemies.remove(first_enemy)
                
                self.cooldown_tracker = 0
                self.arrowX = self.left_coord + self.width/2
                self.arrowY = self.top_coord
                self.right = False
                self.up = False