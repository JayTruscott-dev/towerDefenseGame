import pygame
import os
from .enemy import Enemy


#  ANIMATION IMAGES (MOVEMENT / ATTACK) # M: A: 23-->33
move_imgs = []
attack_imgs = []
# Looking left: Images 23-33
for x in range(23,34,1): # 23 --> 33, 34 --> 13
    add_str = str(x)
    for i in range(2):
        move_imgs.append(pygame.transform.scale(pygame.image.load(os.path.join("media/Enemies/2-Swordsman/Walk", "Manarmswalk0" + add_str + ".png")), (50,50)))
        attack_imgs.append(pygame.transform.scale(pygame.image.load(os.path.join("media/Enemies/2-Swordsman/Attack", "Manarmsattack0" + add_str + ".png")), (80,50)))

for y in range(33,16,-1):
    add_str = str(y)
    if y != 33:
        for i in range(2):
            move_imgs.append(pygame.transform.scale(pygame.image.load(os.path.join("media/Enemies/2-Swordsman/Walk", "Manarmswalk0" + add_str + ".png")), (50,50)))
            #attack_imgs.append(pygame.transform.scale(pygame.image.load(os.path.join("media/Enemies/2-Swordsman/Attack", "Manarmsattack0" + add_str + ".png")), (50,50)))

# ANIMATION IMAGES (DEAD)
dead_imgs = []
for x in range(34,45,1): # 34-->44
    add_str = str(x)
    for i in range(3):
        dead_imgs.append(pygame.transform.scale(pygame.image.load(os.path.join("media/Enemies/2-Swordsman/Die", "Manarmsdie0" + add_str + ".png")), (120,50)))

# Swordsman   (30 HP, 1.0 S,  2 DMG/s, x GP)
class Swordsman(Enemy):
    
    def __init__(self, path):
        super().__init__(path)
        #self.speed = 1.0
        self.SPD = 1.0#self.speed
        self.max_health = 3
        self.health = self.max_health
        self.DMG = 2
        self.coins = 20
        self.width = 50
        self.height = 50
        
        self.imgs = move_imgs[:]
        self.attackImgs = attack_imgs[:]
        self.deadImgs = dead_imgs[:]
        
        self.name = "Swordsman"