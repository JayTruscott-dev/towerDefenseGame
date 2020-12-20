import pygame
import os
from .enemy import Enemy

# MOVEMENT ANIMATION IMAGES
move_imgs = []
# Looking left: Images 21-30
for x in range(25,37,1):  # 23 --> 33, 34 --> 13
    add_str = str(x)
    for i in range(2):
        move_imgs.append(pygame.transform.scale(pygame.image.load(os.path.join("media/Enemies/5-Petard/Walk", "Petardwalk0" + add_str + ".png")), (50,50)))
            
for y in range(36,24,-1):  # 23 --> 33, 34 --> 13
    add_str = str(y)
    if y != 36:
        for i in range(2):
            move_imgs.append(pygame.transform.scale(pygame.image.load(os.path.join("media/Enemies/5-Petard/Walk", "Petardwalk0" + add_str + ".png")), (50,50)))

# ATTACKING ANIMATION IMAGES
attack_imgs = []
dead_imgs = []
# All images
for x in range(1,41,1):
    add_str = str(x)
    for i in range(2):
        if x < 10:
            attack_imgs.append(pygame.transform.scale(pygame.image.load(os.path.join("media/Enemies/5-Petard/Die", "Petarddie00" + add_str + ".png")), (180,160)))
        else:
            dead_imgs.append(pygame.transform.scale(pygame.image.load(os.path.join("media/Enemies/5-Petard/Die", "Petarddie0" + add_str + ".png")), (180,160)))

# Petard (50 HP, 0.5 S, 10 DMG, x GP)
class Petard(Enemy):
    
    def __init__(self, path):
        super().__init__(path)
        #self.speed = 1.2
        self.SPD = 0.8
        self.max_health = 8
        self.health = self.max_health
        self.DMG = 10
        self.coins = 100
        self.width = 50
        self.height = 50
        
        self.imgs = move_imgs[:]
        self.attackImgs = attack_imgs[:]
        self.deadImgs = dead_imgs[:]
        
        self.name = "Petard"