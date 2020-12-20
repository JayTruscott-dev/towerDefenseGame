import pygame
import os
from .enemy import Enemy

# ANIMATION IMAGES (MOVEMENT / ATTACK / DEAD)
move_imgs = []
attack_imgs = []
dead_imgs = []
# Looking left: Images 21-30
for x in range(21,31,1):  # 21 --> 30
    add_str = str(x)
    for i in range(2):
        move_imgs.append(pygame.transform.scale(pygame.image.load(os.path.join("media/Enemies/4-Paladin/Walk", "Paladinwalk0" + add_str + ".png")), (64,64)))
        attack_imgs.append(pygame.transform.scale(pygame.image.load(os.path.join("media/Enemies/4-Paladin/Attack", "Paladinattack0" + add_str + ".png")), (64,64)))
        dead_imgs.append(pygame.transform.scale(pygame.image.load(os.path.join("media/Enemies/4-Paladin/Die", "Paladindie0" + add_str + ".png")), (100,64)))

for y in range(32,15,-1):  # 32 --> 21
    add_str = str(y)
    if y != 32:
        for i in range(2):
            move_imgs.append(pygame.transform.scale(pygame.image.load(os.path.join("media/Enemies/4-Paladin/Walk", "Paladinwalk0" + add_str + ".png")), (64,64)))
            #attack_imgs.append(pygame.transform.scale(pygame.image.load(os.path.join("media/Enemies/4-Paladin/Attack", "Paladinattack0" + add_str + ".png")), (64,64)))
            
class Paladin(Enemy):
    
    def __init__(self, path):
        super().__init__(path)
        #self.speed = 1.1
        self.SPD = 0.9#self.speed
        self.max_health = 10
        self.health = self.max_health
        self.DMG = 5
        self.coins = 50
        
        self.imgs = move_imgs[:]
        self.attackImgs = attack_imgs[:]
        self.deadImgs = dead_imgs[:]
        
        self.name = "Paladin"
        