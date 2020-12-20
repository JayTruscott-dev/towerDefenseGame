import pygame
import os
from .enemy import Enemy

# ANIMATION IMAGES (MOVEMENT / ATTACK / DEAD)
# Looking left: Images 21-30
move_imgs = []
attack_imgs = []
dead_imgs = []
for x in range(21,31,1):  # 21-->31,32-->21 # 23-->33,34-->13
    add_str = str(x)
    for i in range(2):
        move_imgs.append(pygame.transform.scale(pygame.image.load(os.path.join("media/Enemies/3-Light_Cavalry/Walk", "Lightcavwalk0" + add_str + ".png")), (64,64)))
        attack_imgs.append(pygame.transform.scale(pygame.image.load(os.path.join("media/Enemies/3-Light_Cavalry/Attack", "Lightcavattack0" + add_str + ".png")), (64,64)))
        dead_imgs.append(pygame.transform.scale(pygame.image.load(os.path.join("media/Enemies/3-Light_Cavalry/Die", "Lightcavdie0" + add_str + ".png")), (100,64)))

for y in range(31,20,-1):
    add_str = str(y)
    if y != 31:
        for i in range(3):
            move_imgs.append(pygame.transform.scale(pygame.image.load(os.path.join("media/Enemies/3-Light_Cavalry/Walk", "Lightcavwalk0" + add_str + ".png")), (64,64)))
            #attack_imgs.append(pygame.transform.scale(pygame.image.load(os.path.join("media/Enemies/3-Light_Cavalry/Attack", "Lightcavattack0" + add_str + ".png")), (100,64)))
            
# Light_Cavalry (10 HP, 3.0 S,  1 DMG/s, x GP)
class LightCavalry(Enemy):
    
    def __init__(self, path):
        super().__init__(path)
        #self.speed = 0.7
        self.SPD = 1.2#self.speed
        self.max_health = 5
        self.health = self.max_health
        self.DMG = 1
        self.coins = 30
        
        self.imgs = move_imgs[:]
        self.attackImgs = attack_imgs[:]
        self.deadImgs = dead_imgs[:]
        
        self.name = "Light-Cavalry"