import pygame
import pygame_menu
import os
import time
import random

import text as displayer

################## ENEMY CLASS IMPORTS ##################
from enemies.militia import Militia
from enemies.swordsman import Swordsman
from enemies.lightCavalry import LightCavalry
from enemies.paladin import Paladin
from enemies.petard import Petard

################## TOWER CLASS IMPORTS ##################
from towers.scout import Scout
from towers.archer import Archer
from towers.cannon import Cannon
from towers.burning import Burning
from towers.improving import Ranger
from towers.improving import Toughen

################## MENU CLASS IMPORTS ##################
from menu.menu import VerticalMenu, OnOffButton

################## INITIALIZATIONS ##################
pygame.font.init()
pygame.init()

os.environ['SDL_VIDEO_CENTERED'] = '1'

################## UTILITIES ##################
regularFont = pygame.font.Font("./fonts/Square.ttf", 24)
gameOverFont = pygame.font.Font("./fonts/Square.ttf", 72)

################## MUSIC PLAYLIST ##################
#pygame.mixer.set_num_channels(2)
file_path = "media/Music"
musicFiles = []
_gameplayMusic = []
GAME_SONG_END = pygame.USEREVENT + 1 # Ensures a number different from another potential USEREVENT

for i in range(1,10,1):
    music_file = "BG" + str(i) + ".ogg"
    musicFiles.append(music_file)

pygame.mixer.music.set_endevent(GAME_SONG_END)
pygame.mixer.music.load(os.path.join(file_path, musicFiles[0]))


# Put GameOver music list here: Currently not being used
gameover_music = []
for i in range(1,3,1):
    gameover_music.append("GameOver" + str(i) + ".ogg")

# BASE SCREEN INITIALIZATION
width = 1200
height = 700
screen = pygame.display.set_mode((width, height))

GOLDENROD = (218,165, 32)
BROWN_BTN = ( 51, 31,  1)
GOLD_BG   = (207,181, 59)
GREEN     = ( 85,107, 47)

# USER INTERFACE GLOBALS
ui_path = "media/UserInterface"
armor_img = pygame.image.load(os.path.join(ui_path, "Armor.png"))
attack_img = pygame.image.load(os.path.join(ui_path, "Attack.png"))
build_img = pygame.image.load(os.path.join(ui_path, "Build.png"))
castle_img = pygame.image.load(os.path.join(ui_path, "Castle.png"))
coins_img = pygame.image.load(os.path.join(ui_path, "Coins.png"))
lives_img = pygame.image.load(os.path.join(ui_path, "Lives.png"))
range_img = pygame.image.load(os.path.join(ui_path, "Range.png"))

################## BUY-MENU IMAGES ##################
ui_bg = pygame.image.load(os.path.join(ui_path, "menu_bg.png"))
side_ui = pygame.transform.rotate(ui_bg, 90)
side_ui = pygame.transform.scale(side_ui, (120,500))

buy_path = "media/UserInterface/TowerList"
buy_scout = pygame.transform.scale(pygame.image.load(os.path.join(buy_path, "Scout-1.png")).convert_alpha(), (40,60))
buy_archer = pygame.transform.scale(pygame.image.load(os.path.join(buy_path, "Archer-1.png")).convert_alpha(), (40,60))
buy_cannon = pygame.transform.scale(pygame.image.load(os.path.join(buy_path, "Cannon-1.png")).convert_alpha(), (40,60))
buy_ranger = pygame.transform.scale(pygame.image.load(os.path.join(buy_path, "Ranger-1.png")).convert_alpha(), (60,60))
buy_toughen = pygame.transform.scale(pygame.image.load(os.path.join(buy_path, "Toughen-1.png")).convert_alpha(), (60,60))

################## BUTTONS ##################
play_btn = pygame.transform.scale(pygame.image.load(os.path.join(ui_path, "play_icon.png")), (75,75))
sound_btn = pygame.transform.scale(pygame.image.load(os.path.join(ui_path, "music_icon.png")), (75,75))
blank_btn = pygame.transform.scale(pygame.image.load(os.path.join(ui_path, "no_icon.png")), (75,75))

#play_btn = pygame.transform.scale(pygame.image.load(os.path.join(ui_path, "StartWave1.png")), (70,70))

wave_bg = pygame.transform.scale(pygame.image.load(os.path.join(ui_path, "menu_bg.png")), (130, 60))

################## TOWER & WAVE VARIABLES ##################
attack_tower_names = ["scout", "archer", "cannon"]
support_tower_names = ["ranger", "toughen"]

################## WAVE DETAILS ##################
waves = [
    [10, 0, 0, 0, 0],
]
#    [10, 5, 0, 0, 0],
#    [15, 5, 0, 0, 0],
#    [15, 10, 0, 0, 0],
#    [0, 0, 20, 0, 0],
#    [20, 20, 5, 0, 0],
#    [20, 20, 0, 2, 0],
#    [25, 30, 5, 1, 0],
#    [0, 0, 60, 0, 0],
#    [5, 5, 10, 0, 5],
#]
num_militia = 10
num_swords = 0
num_cav = 0
num_paladin = 0
num_petard = 0

class Game():
    def __init__(self, castle_choice, map_choice):
        # GAME SCREEN
        self.width = width
        self.height = height
        self.screen = screen
        
        # MAP CHOICE
        self.top_bounds = []
        self.bottom_bounds = []
        map_choice += 1
        bg = pygame.image.load(os.path.join("media/Maps", "Map" + str(map_choice) + ".png"))
        self.bg = pygame.transform.scale(bg, (self.width, self.height))
        if map_choice == 1:
            self.path = [(9, 221), (177, 233), (272, 277), (534, 274), (610, 210), (643, 99), (726, 52), (807, 91), (855, 233), (971, 280), (1048, 378), (1021, 459), (883, 501), (736, 512), (580, 542), (148, 541), (116, 509)]#, (85, 442)]#, (52, 335)]
            #self.path_collisions = [(4, 183), (2, 264), (144, 182), (143, 265), (186, 191), (163, 273), (212, 202), (181, 282), (231, 217), (194, 298), (253, 233), (209, 312), (273, 236), (234, 322), (526, 237), (527, 323), (538, 233), (546, 319), (551, 225), (563, 315), (562, 216), (577, 307), (571, 204), (593, 298), (576, 190), (606, 286), (579, 171), (618, 274), (580, 152), (628, 262), (582, 134), (638, 251), (586, 119), (645, 239), (591, 105), (652, 224), (597, 92), (657, 210), (607, 80), (660, 192), (616, 67), (661, 177), (624, 59), (663, 161), (634, 49), (666, 145), (646, 40), (671, 130), (658, 33), (683, 117), (671, 27), (693, 109), (686, 21), (706, 103), (702, 16), (722, 101), (722, 13), (722, 13), (737, 101), (737, 15), (750, 105), (756, 18), (762, 111), (770, 20), (773, 120), (784, 25), (782, 133), (797, 32), (790, 147), (810, 40), (792, 164), (824, 51), (794, 180), (836, 65), (795, 197), (845, 78), (799, 211), (855, 92), (804, 227), (863, 106), (812, 243), (869, 123), (820, 257), (873, 138), (830, 269), (876, 157), (841, 280), (875, 172), (852, 291), (880, 189), (864, 298), (887, 205), (877, 304), (896, 218), (888, 311), (906, 228), (899, 315), (921, 233), (912, 318), (936, 235), (927, 321), (952, 235), (943, 320), (968, 239), (960, 323), (987, 244), (977, 328), (1006, 251), (987, 338), (1022, 260), (996, 352), (1037, 272), (1004, 366), (1050, 286), (1007, 384), (1061, 301), (1007, 401), (1071, 317), (1002, 415), (1080, 339), (992, 434), (1089, 369), (979, 447), (1090, 397), (967, 454), (1084, 429), (955, 457), (1076, 453), (942, 459), (1069, 467), (931, 459), (1057, 485), (777, 458), (1047, 498), (764, 460), (1034, 508), (751, 463), (1020, 521), (733, 468), (1003, 529), (714, 478), (984, 539), (694, 487), (964, 543), (686, 497), (951, 546), (673, 503), (767, 544), (666, 510), (751, 552), (650, 514), (737, 561), (185, 514), (727, 576), (170, 511), (711, 586), (157, 504), (691, 594), (150, 500), (189, 599), (145, 492), (162, 595), (154, 484), (143, 589), (165, 480), (123, 579), (176, 477), (109, 572), (189, 474), (93, 560), (200, 469), (84, 549), (201, 352), (74, 536), (171, 337), (64, 523), (103, 308), (58, 512), (69, 322), (54, 497), (26, 337), (2, 471), (24, 385), (1, 399)]
            #self.top_bounds    = [(2, 183), (56, 184), (110, 184), (169, 188), (214, 205), (252, 234), (304, 238), (351, 238), (411, 239), (462, 239), (512, 239), (551, 226), (577, 193), (582, 155), (588, 121), (605, 82), (630, 53), (666, 30), (707, 19), (755, 19), (802, 37), (838, 66), (861, 104), (876, 155), (885, 202), (927, 233), (978, 241), (1025, 265), (1060, 300), (1081, 346), (1086, 408), (1077, 452), (1054, 488), (1020, 516), (981, 537), (931, 543), (880, 543), (832, 542), (785, 543), (742, 558), (696, 589), (641, 597), (587, 598), (536, 599), (486, 598), (432, 598), (381, 600), (327, 603), (283, 603), (228, 602), (178, 597), (129, 584), (96, 558), (70, 529), (53, 493)]
            #self.bottom_bounds = [(3, 266), (52, 266), (104, 265), (146, 268), (188, 289), (225, 315), (273, 321), (317, 320), (362, 320), (365, 320), (415, 321), (473, 323), (526, 321), (565, 312), (598, 288), (628, 261), (651, 227), (659, 169), (679, 127), (711, 104), (756, 105), (791, 145), (796, 202), (815, 244), (845, 280), (878, 308), (925, 323), (971, 329), (1008, 376), (1001, 423), (967, 450), (917, 459), (872, 458), (821, 458), (774, 457), (730, 471), (694, 493), (659, 511), (592, 515), (533, 515), (483, 515), (439, 514), (400, 514), (356, 514), (312, 514), (274, 513), (237, 513), (203, 515), (162, 507), (146, 489), (127, 448), (125, 445), (123, 444), (120, 440), (118, 435)]
            self.castle_pos = (1, 305)
        elif map_choice == 2:
            #self.path = [(1, 524), (146, 522), (199, 466), (226, 354), (294, 307), (383, 281), (417, 197), (463, 100), (520, 80), (755, 79), (820, 60), (883, 79), (1048, 86), (1103, 153), (1105, 232), (1031, 300), (936, 335), (897, 415), (942, 506), (1039, 529), (1106, 591), (1117, 694), (1250,800)]
            self.path = [(1, 524), (146, 522), (199, 466), (226, 354), (294, 307), (383, 281), (417, 197), (463, 100), (520, 80), (755, 79), (820, 60), (883, 79), (1048, 86), (1103, 153), (1105, 232), (1031, 300), (936, 335), (897, 415), (942, 506)]#, (1039, 529), (1106, 591)]
            self.path_collisions = []
            self.castle_pos = (997,494)
        
        # CASTLE CHOICE
        castle_choice += 1
        castle = pygame.image.load(os.path.join("media/Castles", "Castle" + str(castle_choice) + ".png"))
        self.castle = pygame.transform.scale(castle, (200,200))
        
        # ENEMYS
        self.enemys = [] 

        # TOWERS
        self.attack_towers = []
        self.support_towers = []
        self.selected_tower = None
        
        self.moving_object = None
        
        # MUSIC
        self.file_path = "media/Music"
        self.game_music = musicFiles[:]
        
        # WAVES
        self.wave = 0
        self.wave_copy = waves[:]
        self.current_wave = self.wave_copy[self.wave][:]
        
        # GAME ATTRIBUTES
        self.coins = 90000
        self.lives = 100
        self.enemies_defeated = 0
        self.coins_earned = 0
        
        # IN-GAME MENU
        self.menu = VerticalMenu(self.width - side_ui.get_width() + 70, 250, side_ui)
        self.menu.add_btn(buy_scout, "buy_scout", 500)
        self.menu.add_btn(buy_archer, "buy_archer", 750)
        self.menu.add_btn(buy_cannon, "buy_cannon", 1000)
        self.menu.add_btn(buy_ranger, "buy_ranger", 1500)
        self.menu.add_btn(buy_toughen, "buy_toughen", 1500)
        
        self.pause = True
        self.music_on = True
        self.playPauseButton = OnOffButton(play_btn, blank_btn, 10, self.height - 85)
        self.soundButton = OnOffButton(sound_btn, blank_btn, 90, self.height - 85)
        
        # GAME OVER
        self.playing_again = None
        self.lose_music = gameover_music[:]
        
        # TIMING
        self.timer = time.time()
        self.counter = 0

    def generateWave(self):
        """
        Generates the next wave of enemies to send (uses next wave's divisibility to build each enemy type)
        Params: None
        Return: None
        """
        global waves, num_militia, num_swords, num_cav, num_paladin, num_petard
        if sum(self.current_wave) == 0:
            if len(self.enemys) == 0:
                
                next_wave = self.wave + 1
                if next_wave % 10 == 0:
                    num_petard += 2
                if next_wave % 8 == 0:
                    num_paladin += 6
                if next_wave % 5 == 0:
                    num_paladin += 3
                if next_wave % 3 == 0:
                    num_cav += 5
                if next_wave % 2 == 0:
                    num_swords += 10
                else:
                    num_militia += 10
                
                waves.append([num_militia, num_swords, num_cav, num_paladin, num_petard])
                self.wave_copy.append([num_militia, num_swords, num_cav, num_paladin, num_petard])
                
                self.wave += 1
                self.current_wave = waves[self.wave]
                self.pause = True
                self.playPauseButton.paused = self.pause
        else:
            wave_enemies = [Militia(self.path), Swordsman(self.path), LightCavalry(self.path), Paladin(self.path), Petard(self.path)]
            for x in range(len(self.current_wave)):
                if self.current_wave[x] != 0: # Checks if wave object list has remaining numbers to generate
                    self.enemys.append(wave_enemies[x]) # Appends this enemy to the enemys list
                    self.current_wave[x] = self.current_wave[x] - 1 # Decrements the amount of that enemy type from the object list
                    break

    def run(self):
        run = True
        clock = pygame.time.Clock()
        while run:
            clock.tick(40)
            
            # Player earns coins for surviving each wave
            if len(self.enemys) == 0 and self.counter == 0:
                self.coins += 100*self.wave
                self.coins_earned += 100*self.wave
                self.counter += 1
            
            if self.pause == False:
                
                if time.time() - self.timer > random.randrange(2,8)/3:
                    self.timer = time.time()
                    self.generateWave()
                    self.counter = 0
            
            pos = pygame.mouse.get_pos()
            towerToDelete = []
            
            # Checks for moving an object
            if self.moving_object:
                self.moving_object.move(pos[0], pos[1])
                tower_list = self.attack_towers[:] + self.support_towers[:]
                collide = False
                for tower in tower_list:
                    if tower.collide(self.moving_object):
                        collide = True
                        tower.place_color = (255, 0, 0, 100)
                        self.moving_object.place_color = (255, 0, 0, 100)
                    else:
                        tower.place_color = (0, 0, 255, 100)
                        if not collide:
                            self.moving_object.place_color = (0, 0, 255, 100)
            
            # Main pygame event loop
            for event in pygame.event.get():
                if event.type == GAME_SONG_END:
                    self.play_next_song()
                if event.type == pygame.QUIT:
                    run = False
                
                if event.type == pygame.MOUSEBUTTONUP:
                    # Checks for moving an object and clicking
                    if self.moving_object:
                        not_allowed = False
                        tower_list = self.attack_towers[:] + self.support_towers[:]
                        for tower in tower_list:
                            if tower.collide(self.moving_object):
                                not_allowed = True
                        
                        if not not_allowed and self.point_to_line(self.moving_object):
                            if self.moving_object.name in attack_tower_names:
                                self.attack_towers.append(self.moving_object)
                            elif self.moving_object.name in support_tower_names:
                                self.support_towers.append(self.moving_object)
                            
                            self.moving_object.moving = False
                            self.moving_object = None
                        
                    else:
                        # Checks for interaction with Start Wave button
                        if self.playPauseButton.click(pos[0], pos[1]):
                            if self.pause and len(self.enemys) == 0:
                                self.pause = not(self.pause) # Acts as a toggle Boolean 
                            self.playPauseButton.paused = self.pause
                        # Checks for interaction with Sound/Mute button
                        if self.soundButton.click(pos[0], pos[1]):
                            self.music_on = not(self.music_on)
                            self.soundButton.paused = self.music_on
                            if self.music_on:
                                pygame.mixer.music.unpause()
                            else:
                                pygame.mixer.music.pause()
                        
                        # Checks for interaction with sidebar menu
                        side_menu_button = self.menu.get_clicked(pos[0], pos[1])
                        if side_menu_button:
                            cost = self.menu.get_item_cost(side_menu_button)
                            if self.coins >= cost:
                                self.coins -= cost
                                self.add_tower(side_menu_button)
                        
                        # Checks for interaction with towers based on type (attack or support)
                        btn_clicked = None
                        if self.selected_tower:
                            btn_clicked = self.selected_tower.menu.get_clicked(pos[0], pos[1])
                            if btn_clicked:
                                if btn_clicked == "Upgrade":
                                    cost = self.selected_tower.get_upgrade_cost()
                                    if cost != "MAX":
                                        if self.coins >= cost:
                                            self.coins -= cost
                                            self.selected_tower.upgrade()
                                elif btn_clicked == "Sell":
                                    price = self.selected_tower.get_sell_price()
                                    self.coins += price
                                    if self.selected_tower.name in attack_tower_names:
                                        for tw in self.attack_towers:
                                            if self.selected_tower.collide(tw):
                                                self.attack_towers.remove(tw)
                                                break
                                    elif self.selected_tower.name in support_tower_names:
                                        for tw in self.support_towers:
                                            if self.selected_tower.collide(tw):
                                                self.support_towers.remove(tw)
                                                break
                                    self.selected_tower = None
                                    btn_clicked = None
                        
                        if not(btn_clicked):
                            for tw in self.attack_towers:
                                if tw.click(pos[0], pos[1]):
                                    tw.selected = True
                                    self.selected_tower = tw
                                else:
                                    tw.selected = False
                            for tw in self.support_towers:
                                if tw.click(pos[0], pos[1]):
                                    tw.selected = True
                                    self.selected_tower = tw
                                else:
                                    tw.selected = False

            # WAVE GAMEPLAY
            if not self.pause:
                
                # Loops through all tower actions (attack or improve)
                for tw in self.attack_towers:
                    earnings = 0
                    tw.cooldown_tracker += clock.get_time()
                    if tw.cooldown_tracker >= tw.speed:
                        #self.coins += tw.attack(self.enemys)
                        earnings = tw.attack(self.enemys)
                        self.coins_earned += earnings
                        self.coins += earnings
                    
                    for t in self.support_towers:
                        if t.collideRNG(tw):
                            if t.name == "ranger":
                                addedRange = t.improve(tw.original_range)
                                tw.change_range(addedRange)
                            elif t.name == "toughen":
                                addedDamage = t.improve(tw.original_damage)
                                tw.change_damage(addedDamage)
                
            # Checks for game over (lives <= 0)
            if self.lives <= 0:
                run = False
                pygame.mixer.music.stop()
                self.playing_again = self.gameOver(self.screen)
                
            self.draw()
        
        pygame.display.update()
        
        return self.playing_again
    
    def point_to_line(self, tower):
        """ Checks for tower placement distance from the path. This function is not currently implemented in the project
            Params: tower (object): Tower trying to be placed
            Return: Bool
        """
        for x, point in enumerate(self.top_bounds):
            bisect_b = self.bottom_bounds[x]
            
            # Check if tower.x collides along line from point (x1,y1) to bisect_b (x2,y2)
        return True
    
    def draw(self):
        """ Draws enemy list & tower list to the screen. Contains display updater
            Params: None
            Return: None
        """
        self.screen.blit(self.bg, (0,0))
        
        # PLAYER CASTLE DRAW
        self.screen.blit(self.castle, (self.castle_pos))
        
        # ENEMY DRAW
        toDelete = []
        for e in self.enemys:
            if not e.has_died:
                if e.atCastle:
                    self.lives -= e.draw_attack(self.screen)
                else:
                    e.draw(self.screen)
            else:
                e.draw_death(self.screen)
                if e.dead_complete:
                    toDelete.append(e)
                    self.enemies_defeated += 1
        
        for d in toDelete:
            self.enemys.remove(d)
        
        # TOWER PLACEMENT CIRCLE DRAW
        if self.moving_object:
            for tower in self.attack_towers:
                tower.draw_placement(self.screen)
            
            for tower in self.support_towers:
                tower.draw_placement(self.screen)
            
            self.moving_object.draw_placement(self.screen)
        
        # TOWER DRAWS
        for tw in self.attack_towers:
            tw.draw(self.screen)
            
        for tw in self.support_towers:
            tw.draw(self.screen)
        
        # Redraws a selected tower to the screen
        if self.selected_tower:
            self.selected_tower.draw(self.screen)
        
        # Draws the currently moving object to the screen
        if self.moving_object:
            self.moving_object.draw(self.screen)
        
        # VERTICAL MENU DRAW
        self.menu.draw(self.screen)
        
        # START WAVE & MUSIC TOGGLE BUTTONS DRAW
        self.playPauseButton.draw(self.screen)
        self.soundButton.draw(self.screen)
        
        # WAVE TITLECARD DRAW
        wave_text = "Wave # " + str(self.wave + 1)
        wave_surf, wave_rect = displayer.display_text(wave_text, regularFont, GOLDENROD, 10 + wave_bg.get_width()/2, 10 + wave_bg.get_height()/2)
        if self.wave + 1 >= 100: # Keeps wave # from spilling right of wave_bg image
            pygame.transform.scale(wave_bg, (140,60))
        self.screen.blit(wave_bg, (10,10))
        self.screen.blit(wave_surf, (wave_rect[0], wave_rect[1]))
        
        # PLAYER VALUES (LIVES, COINS)
        margin = 10
        # - IMAGES
        self.screen.blit(lives_img, (1168, 10, 22, 22))
        self.screen.blit(coins_img, (1168, 42, 22, 22))
        
        # - STRINGS
        lives_text = str(self.lives)
        coins_text = str(self.coins)
        
        lives_digits = len(lives_text)
        coins_digits = len(coins_text)
        
        center_lives_x = int(1158 - (5*lives_digits))
        center_coins_x = int(1158 - (5*coins_digits))
        
        l = 10*lives_digits
        c = 10*coins_digits
        
        lives_surf, lives_rect = displayer.display_text(lives_text, regularFont, GOLDENROD, center_lives_x, 21)
        coins_surf, coins_rect = displayer.display_text(coins_text, regularFont, GOLDENROD, center_coins_x, 53)
        
        self.screen.blit(lives_surf, (1158-lives_rect[2], 10, l, 22))
        self.screen.blit(coins_surf, (1158-coins_rect[2], 42, c, 22))
        
        pygame.display.update()
    
    def add_tower(self, name):
        x, y = pygame.mouse.get_pos()
        name_list = ["buy_scout", "buy_archer", "buy_cannon", "buy_ranger", "buy_toughen"]
        object_list = [Scout(x,y), Archer(x,y), Cannon(x,y), Ranger(x,y), Toughen(x,y)]
        
        try:
            obj = object_list[name_list.index(name)]
            self.moving_object = obj
            obj.moving = True
            obj.update_projectile()
        except Exception as e:
            print(str(e) + " NOT VALID NAME")
            
    def play_next_song(self):
        """ This function handles the music playlist looping for multiple songs
            Params: None
            Return: None
        """
        if self.lives > 0:
            self.game_music = musicFiles[1:]
            self.game_music.append(musicFiles[0])
        else:
            self.game_music = gameover_music[1:]
            self.game_music.append(gameover_music[0])
            
        pygame.mixer.music.load(os.path.join(file_path, self.game_music[0]))
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play()
        
    
    def gameOver(self, window):
        """ This function handles user interaction once they run out of lives.
            Params: window (Surface): surface used for blitting
            Return: Bool: True to return to the main menu, False to exit completely
        """
        global waves
        
        waves = [[10, 0, 0, 0, 0],]
        self.coins = 900
        self.attack_towers = []
        self.support_towers = []
        
        pygame.mixer.music.load(os.path.join(file_path, self.lose_music[0]))
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)
        
        while True:
            self.playing_again = None
            # Rect -> (left, top, width, height)
            #GOLDENROD = (218,165,32)
            #BROWN_BTN = (51,31,1)
            #GOLD_BG = (207,181,59)
            
            window.blit(self.bg, (0,0))
            
            # Titlecard background fill variables
            tcard_x = self.width / 4 # Left Margin of 1/4 self.width --> 300
            tcard_y = 100 # Top Margin of 1/3 self.height --> 100 + 500 + 100 = 700
            tcard_w = tcard_x * 2 # 600 wide titlecard
            tcard_h = 500 # 500 high titlecard
            over_bg = pygame.Surface((tcard_w,tcard_h), pygame.SRCALPHA, 32)
            over_bg.fill((GREEN))
            window.blit(over_bg, (tcard_x,tcard_y))
            
            message1 = "GAME OVER"
            m1X = int(self.width/2)
            m1Y = int(self.height/2 - 150)
            overTextSurf, overTextRect = displayer.display_text(message1, gameOverFont, (0,0,0), m1X, m1Y) # C = (600, 200)
            window.blit(overTextSurf, overTextRect)
            
            score_message = "Highest Wave Completed: #" + str(self.wave)
            scoreTextSurf, scoreTextRect = displayer.display_text(score_message, regularFont, (0,0,0), m1X, m1Y+100) # C = (600, 300)
            window.blit(scoreTextSurf, scoreTextRect)
            
            score_message = "Total Enemies Defeated: " + str(self.enemies_defeated)
            scoreTextSurf, scoreTextRect = displayer.display_text(score_message, regularFont, (0,0,0), m1X, m1Y+131) # C = (600, 300)
            window.blit(scoreTextSurf, scoreTextRect)
            
            score_message = "Total Coins Earned: " + str(self.coins_earned)
            scoreTextSurf, scoreTextRect = displayer.display_text(score_message, regularFont, (0,0,0), m1X, m1Y+162) # C = (600, 300)
            window.blit(scoreTextSurf, scoreTextRect)
            
            r_message = "RETURN TO MENU"
            r_btn_rect = pygame.Rect(350, 477, 201, 46) # 450 - 100 = 350, 500 - 46/2 = 477
            window.fill((BROWN_BTN), r_btn_rect)
            replayTextSurf, replayTextRect = displayer.display_text(r_message, regularFont, GOLDENROD, 450, 500) # C = (450, 500)
            window.blit(replayTextSurf, replayTextRect)
            
            q_message = "QUIT GAME"
            q_btn_rect = pygame.Rect(720, 477, 130, 46)
            window.fill((BROWN_BTN), q_btn_rect)
            quitTextSurf, quitTextRect = displayer.display_text(q_message, regularFont, GOLDENROD, 785, 500) # C = (785, 500)
            window.blit(quitTextSurf, quitTextRect)
            
            # Mouse event checker
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    
                    if quitTextRect.collidepoint(pos):
                        self.playing_again = False
                        
                    elif replayTextRect.collidepoint(pos):
                        self.playing_again = True

            if not self.playing_again is None:
                break
            
            pygame.display.flip()
        
        return self.playing_again


