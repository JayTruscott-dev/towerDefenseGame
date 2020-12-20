import pygame
import math

class Enemy:

    def __init__(self, path):
        """ Initialize Enemy with the following attributes.
            Params: path (list): list of each path point for the enemy to traverse
        """
        # IMAGES
        self.width = 64
        self.height = 64
        self.animation_count = 0
        self.img = None
        self.imgs = []
        self.flipped = False
        
        # ATTACKING
        self.ATK_animations = 0
        self.attackImgs = []
        self.attackImg = None
        
        # DYING
        self.DEAD_animations = 0
        self.deadImgs = []
        self.deadImg = None
        self.has_died = False
        self.dead_complete = False
        self.dead_x = 0
        self.dead_y = 0
        
        # HEALTH
        self.health = 1
        self.max_health = 0
        
        # SPEED
        self.speed = 1
        self.speed_increase = 1.2
        self.SPD = 1
        
        # MAPPING
        self.path = path
        
        # POSITIONING
        self.x = self.path[0][0]
        self.y = self.path[0][1]
        self.dis = 0
        self.path_pos = 0
        self.move_count = 0
        self.move_dis = 0
        
        # AT CASTLE CHECK
        self.atCastle = False
        
        
    def draw(self, screen):
        """ Draws the enemy with the given images
            Params: screen (Surface): surface used for blitting
            Return: None
        """
        self.img = pygame.transform.flip(self.imgs[self.animation_count//3], True, False)
        
        self.animation_count += 1
        if self.animation_count >= len(self.imgs*3):
            self.animation_count = 0
        
        newWidth = int(self.x) - self.img.get_width()/2
        newHeight = int(self.y) - self.img.get_height()/2 - 20
        if self.path_pos + 1 < len(self.path):
            screen.blit(self.img, (newWidth, newHeight))

            self.draw_health_bar(screen)
            self.move()
                
        elif self.path_pos + 1 >= len(self.path):
            self.atCastle = True
        
    def draw_attack(self, screen):
        self.attackImg = pygame.transform.flip(self.attackImgs[self.ATK_animations//3], False, False)
        
        amount_attacked = 0
        self.ATK_animations += 1
        if self.ATK_animations >= len(self.attackImgs*3):
            amount_attacked = self.DMG
            self.ATK_animations = 0
        
        self.x = self.path[-1][0]
        self.y = self.path[-1][1]
        newX = int(self.x - self.attackImg.get_width()/2)
        newY = int(self.y - self.attackImg.get_height()/2)
        screen.blit(self.attackImg, (newX, newY))
        
        #self.draw_health_bar(screen)
        
        return amount_attacked
        
    def draw_death(self, screen):
        """
        This function was not implemented within the scope of this project, hopefully it'll be utilized later on
        Params: screen (Surface): surface used for blitting animations
        Return: None
        """
        self.deadImg = pygame.transform.flip(self.deadImgs[self.DEAD_animations], not(self.flipped), False)
        
        self.DEAD_animations += 1
        if self.DEAD_animations >= len(self.deadImgs):
            self.dead_complete = True
            self.DEAD_animations = 0
        
        newX = int(self.x - self.deadImg.get_width()/2)
        newY = int(self.y - self.deadImg.get_height()/2) - 10
        if not(self.dead_complete):
            screen.blit(self.deadImg, (newX, newY))
        
    def draw_health_bar(self, screen):
        """ Draws the health bar above each enemy
            Param: screen (Surface): The game screen
            Return: None
        """
        length = 50
        move_by = round(length / self.max_health)
        health_bar = move_by * self.health
        
        pygame.draw.rect(screen, (255,0,0), (self.x-30, self.y-75, length, 10), 0)
        pygame.draw.rect(screen, (0,255,0), (self.x-30, self.y-75, health_bar, 10), 0)

    def collide(self, X, Y):
        """ Collision detection with enemy image
            Params: X (int): enemy x coord
                    Y (int): enemy y coord
            Return: Bool
        """
        if X <= self.x + (self.width/2) and X >= self.x:
            if Y <= self.y + (self.height/2) and Y >= self.y:
                return True
        return False
    
    def move(self):
        """ Contains pathing algorithm for enemies moving between path points
            Params: None
            Return: None
        """
        self.animation_count += 1
        if self.animation_count >= len(self.imgs):
            self.animation_count = 0
        
        x1, y1 = self.path[self.path_pos]
        
        if self.path_pos + 1 < len(self.path):
            x2, y2 = self.path[self.path_pos + 1]
        else:
            x2, y2 = self.path[self.path_pos]
        
        dirn = ((x2-x1), (y2-y1))
        length = (math.sqrt((dirn[0])**2 + (dirn[1])**2))
        dirn = (dirn[0], dirn[1])
        dirn = (dirn[0]/length, dirn[1]/length)
        
        if dirn[0] < 0 and not(self.flipped):
            self.flipped = True
            for x, img in enumerate(self.imgs):
                self.imgs[x] = pygame.transform.flip(img, True, False)
        
        move_x, move_y = ((self.x + dirn[0]), (self.y + dirn[1]))
        
        self.x = move_x
        self.y = move_y
        
        # Go to next point
        if dirn[0] >= 0: # For moving to the right
            if dirn[1] >= 0: # For moving down
                if self.x >= x2 and self.y >= y2:
                    self.path_pos += 1
            else:
                if self.x >= x2 and self.y <= y2:
                    self.path_pos += 1
        else: # For moving to the left
            if dirn[1] >= 0: # For moving down
                if self.x < x2 and self.y >= y2:
                    self.path_pos += 1
            else:
                if self.x < x2 and self.y >= y2:
                    self.path_pos += 1
        
    def died(self, DMG):
        """ Removes enemy health each call
            Params: DMG (int): DMG that a tower inflicts
            Return: Bool
        """
        self.health -= DMG
        if self.health <= 0:
            self.has_died = True
            return True