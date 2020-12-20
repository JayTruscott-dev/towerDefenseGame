import pygame
import os
from .enemy import Enemy

# ANIMATION IMAGES (MOVEMENT)
move_imgs = []
for x in range(25,37,1):
    add_str = str(x)
    for i in range(2):
        move_imgs.append(pygame.transform.scale(pygame.image.load(os.path.join("media/Enemies/1-Militia/Walk", "Militiawalk0" + add_str + ".png")), (50,50)))
for y in range(36,14,-1):
    add_str = str(y)
    if y != 37:
        for i in range(2):
            move_imgs.append(pygame.transform.scale(pygame.image.load(os.path.join("media/Enemies/1-Militia/Walk", "Militiawalk0" + add_str + ".png")), (50,50)))

# ANIMATION IMAGES (ATTACK)
attack_imgs = []
for x in range(20,31,1):
    add_str = str(x)
    for i in range(2):
        attack_imgs.append(pygame.transform.scale(pygame.image.load(os.path.join("media/Enemies/1-Militia/Attack", "Militiaattack0" + add_str + ".png")), (80,50)))
#for y in range(29,19,-1):
#    add_str = str(y)
#    for i in range(2):
#        attack_imgs.append(pygame.transform.scale(pygame.image.load(os.path.join("media/Enemies/1-Militia/Attack", "Militiaattack0" + add_str + ".png")), (50,50)))

# ANIMATION IMAGES (DEAD)
dead_imgs = []
for x in range(21,31,1):
    add_str = str(x)
    for i in range(3):
        dead_imgs.append(pygame.transform.scale(pygame.image.load(os.path.join("media/Enemies/1-Militia/Die", "Militiadie0" + add_str + ".png")), (120,50)))

class Militia(Enemy):
    
    def __init__(self, path):
        super().__init__(path)
        #self.speed = 1.1
        self.SPD = 1.1#self.speed
        self.max_health = 1
        self.health = self.max_health
        self.DMG = 1
        self.coins = 10
        self.width = 50
        self.height = 50
        
        self.imgs = move_imgs[:]
        self.attackImgs = attack_imgs[:]
        self.deadImgs = dead_imgs[:]
        
        self.name = "Militia"