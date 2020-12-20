import pygame
import os, sys
import math
import pygame_menu

import game as play_game

pygame.init()
# BASE SCREEN INITIALIZATION
width = 1200
height = 700
screen = pygame.display.set_mode((width, height))

os.environ['SDL_VIDEO_CENTERED'] = '1'

# COLORING
# (#DAA520)
GOLDENROD   = (218,165, 32) # Box (Selected)
# (#FFD700)
GOLD        = (255,215,  0) # Menu Border
# (#CFB53B)
OLDGOLD     = (207,181, 59) # Box (Unselected)
# (#996515)
GOLDENBROWN = (153,101, 21) # Unused?
# (#000000)
BLACK       = (  0,  0,  0) # For Other
# (#FFFFFF)
WHITE       = (255,255,255) # For Text
# (#B2AC88)
GREEN       = ( 85,107, 47)

# Start with copy of THEME_ORANGE
medieval_THEME = pygame_menu.themes.THEME_ORANGE.copy()

# Redefine background as Image
menu_bg = pygame_menu.baseimage.BaseImage(
            image_path=os.path.join('media/Menu', 'BG.png'),
            drawing_mode=pygame_menu.baseimage.IMAGE_MODE_FILL,
            drawing_offset=(0,0)
        )
medieval_THEME.background_color = menu_bg
medieval_THEME.widget_background_color = GREEN
# Remove TitleCard Styling
medieval_THEME.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_NONE
# Remove X Button
medieval_THEME.menubar_close_button = True
# New Fonts
medieval_THEME.title_font = pygame_menu.font.FONT_PT_SERIF
medieval_THEME.title_font_color = BLACK
medieval_THEME.widget_font = pygame_menu.font.FONT_PT_SERIF
medieval_THEME.widget_font_color = BLACK
# New Sizing
medieval_THEME.title_font_size = 64
medieval_THEME.widget_font_size = 14
# Center Content 
medieval_THEME.title_offset = (400,0)
medieval_THEME.widget_alignment = pygame_menu.locals.ALIGN_CENTER


start_menu = pygame_menu.Menu(height=700,
                              width=1200,
                              title="Medieval Age",
                              center_content=True,
                              column_force_fit_text=False,
                              column_max_width=None,
                              columns=1,
                              enabled=True,
                              joystick_enabled=True,
                              menu_id='main',
                              menu_position=(50,50),
                              mouse_enabled=True,
                              mouse_motion_selection=True,
                              mouse_visible=True,
                              rows=7,
                              theme=medieval_THEME)

#medieval_THEME.widget_font_size = 14
medieval_THEME.background_color = GREEN

info_menu = pygame_menu.Menu(height=700,
                              width=1200,
                              title="Information",
                              center_content=True,
                              column_force_fit_text=False,
                              column_max_width=None,
                              columns=6,
                              enabled=True,
                              joystick_enabled=True,
                              menu_id='info',
                              menu_position=(50,50),
                              mouse_enabled=True,
                              mouse_motion_selection=True,
                              mouse_visible=True,
                              onclose=pygame_menu.events.BACK,
                              rows=9,
                              theme=medieval_THEME)

# MUSIC
file_path = "media/Music"
pygame.mixer.music.stop()
pygame.mixer.music.load(os.path.join(file_path, "MainMenu.ogg"))
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)

# GLOBAL VARIABLES FOR MENU CHOICES (MAP, CASTLE)
castle_imgs = []
map_imgs = []
for i in range(1,6,1):
    castle_imgs.append(pygame.transform.scale(pygame.image.load(os.path.join("media/Castles", "Castle" + str(i) + ".png")), (350,350)))
#for i in range(1,4,1):
#    map_imgs.append(pygame.transform.scale(pygame.image.load(os.path.join("media/Maps", "Map" + str(i) + ".png")), (340,340)))
map_imgs.append(pygame.transform.scale(pygame.image.load(os.path.join("media/Maps", "Map1.png")), (340,340)))

castle_choice = 0
map_choice = 0

cursor_image = pygame.image.load(os.path.join('media/UserInterface', 'Cursor.png'))

# GAME SETTINGS (Map, Castle, play_again)
settings = [1,1]
play_again = False


def game_settings():
    """
    Return: None
    """
    global play_again
    
    pygame.mixer.music.stop()
    g = play_game.Game(castle_choice, map_choice)
    play_again = g.run()
    
    if play_again == True:
        returnToMenu()
    else:
        quitter()
    
def builder(value, type_val, actual_value):
    # type: C / M
    # Actual Value: 1-5 / 1-5
    global settings, castle_choice, map_choice
    if type_val == "C":
        settings[0] = actual_value
        castle_choice = actual_value - 1
    elif type_val == "M":
        settings[1] = actual_value
        map_choice = actual_value - 1

def infoPage():
    """
    Create information page with pygame_menu library
    Params: None
    Return: None
    """
    global info_menu, start_menu
    
    # Stop Main Menu music, play Info Menu music
    pygame.mixer.music.stop()
    pygame.mixer.music.load(os.path.join("media/Music", "InfoMenu.ogg"))
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1)
    
    start_menu.disable()
    info_menu.enable()
    
    running = True
    while running:
        screen.fill(GOLDENROD)
    
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                quitter()
            
        if info_menu.is_enabled():
            info_menu.update(events)
            info_menu.draw(screen)

        pygame.mouse.set_visible(False)
        cursor_rect = pygame.mouse.get_pos()
        screen.blit(cursor_image, cursor_rect)
    
        pygame.display.update()
    
def returnToMenu():
    """ Resets all choice global variables before regenerating the menu
        Params: None
        Return: None
    """
    global settings, info_menu, start_menu
    settings[0] = 1
    settings[1] = 1
    
    info_menu.disable() # Works as essential 'back button' from Information Menu
    start_menu.enable()
    
    mainMenu(start_menu, info_menu) # Regenerates main_menu from start
    
def quitter():
    """ Handles user interaction for not replaying the game after it ends
        Params: None
        Return: None
    """
    pygame.quit()
    sys.exit()

# MENU BOX MODEL
#   COLUMN 1              COLUMN 2            COLUMN 3
#    EMPTY               LABEL (T2)            EMPTY
#  Selector (C)            EMPTY             Selector (M)
#   C Image                INFO               M Image
#    PLAY                  EMPTY               QUIT

start_menu.add_label("Castle Defender", max_char=-1, font_size=32, background_color=GREEN, font_color=BLACK, margin=(0,8))
start_menu.add_vertical_margin(75)
start_menu.add_selector(title="Castle Type: ", items=[("Germanic", "C", 1), ("Japanese", "C", 2), ("Arabic", "C", 3), ("Frankish", "C", 4), ("Aztec", "C", 5)], default=0, onchange=builder, onreturn=None, selector_id="castles", font_size=24)
#start_menu.add_selector(title="Map: ", items=[("Desert", "M", 1), ("Dark Marsh", "M", 2), ("Winter", "M", 3), ("Retro 1", "M", 4), ("Retro 2", "M", 5)], default=0, onchange=builder, onreturn=None, selector_id="maps")
start_menu.add_selector(title="Map: ", items=[("Desert", "M", 1), ("Desert", "M", 1)], default=0, onchange=builder, onreturn=None, selector_id="maps", font_size=24)
start_menu.add_button(title="INFORMATION", action=infoPage, selection_effect=pygame_menu.widgets.HighlightSelection(border_width=1, margin_x=16.0, margin_y=8.0), align=pygame_menu.locals.ALIGN_CENTER, font_size=24)
start_menu.add_button(title="PLAY GAME", action=game_settings, selection_effect=pygame_menu.widgets.HighlightSelection(border_width=1, margin_x=16.0, margin_y=8.0), align=pygame_menu.locals.ALIGN_CENTER, font_size=24)
start_menu.add_button(title="QUIT GAME", action=quitter, selection_effect=pygame_menu.widgets.HighlightSelection(border_width=1, margin_x=16.0, margin_y=8.0), align=pygame_menu.locals.ALIGN_CENTER, font_size=24)

start_menu.center_content()

# INFO MENU BOX MODEL
#    TOWERS         ENEMIES     GAME ATTRIBUTES
#    SCOUT          MILITIA       
#    ARCHER        SWORDSMAN      
#    CANNON        LIGHT-CAV      
#    RANGER         PALADIN       
#    TOUGHEN        PETARD
ui_path = "media/UserInterface"

################### COLUMN 1 ###################
# Tower Thumbnail Images (Spacer, Scout, Archer, Cannon, Burning, Spacer, Spacer, Spacer)
#info_menu.add_image(os.path.join(ui_path, "TowerList/Archer1.png"), angle=0, image_id="row1Spacer1", scale=(0.05,0.05), scale_smooth=False, selectable=False, align=pygame_menu.locals.ALIGN_RIGHT)
info_menu.add_vertical_margin(33)
info_menu.add_image(os.path.join(ui_path, "TowerList/Scout1.png"), angle=0, image_id='ScoutI', scale=(1.05,1.05), scale_smooth=False, selectable=False, align=pygame_menu.locals.ALIGN_RIGHT, margin=(5,5))
info_menu.add_image(os.path.join(ui_path, "TowerList/Archer1.png"), angle=0, image_id='ArcherI', scale=(1.05,1.05), scale_smooth=False, selectable=False, align=pygame_menu.locals.ALIGN_RIGHT, margin=(5,5))
info_menu.add_image(os.path.join(ui_path, "TowerList/Cannon1.png"), angle=0, image_id='CannonI', scale=(1.05,1.05), scale_smooth=False, selectable=False, align=pygame_menu.locals.ALIGN_RIGHT, margin=(5,5))
info_menu.add_image(os.path.join(ui_path, "TowerList/Ranger-1.png"), angle=0, image_id='RangerI', scale=(0.26,0.26), scale_smooth=False, selectable=False, align=pygame_menu.locals.ALIGN_RIGHT, margin=(4,7))
info_menu.add_image(os.path.join(ui_path, "TowerList/Toughen-1.png"), angle=0, image_id="ToughenI", scale=(0.26,0.26), scale_smooth=False, selectable=False, align=pygame_menu.locals.ALIGN_RIGHT, margin=(4,7))
#info_menu.add_image(os.path.join(ui_path, "TowerList/Archer1.png"), angle=0, image_id="row7Spacer1", scale=(0.05,0.05), scale_smooth=False, selectable=False, align=pygame_menu.locals.ALIGN_RIGHT)
info_menu.add_vertical_margin(5)
#info_menu.add_image(os.path.join(ui_path, "TowerList/Archer1.png"), angle=0, image_id="row8Spacer1", scale=(0.05,0.05), scale_smooth=False, selectable=False, align=pygame_menu.locals.ALIGN_RIGHT)
info_menu.add_vertical_margin(5)
#info_menu.add_image(os.path.join(ui_path, "TowerList/Archer1.png"), angle=0, image_id="row9Spacer1", scale=(0.05,0.05), scale_smooth=False, selectable=False, align=pygame_menu.locals.ALIGN_RIGHT)
info_menu.add_vertical_margin(5)

################### COLUMN 2 ###################
# Tower Descriptions (Title, Scout, Archer, Cannon, Burning, Spacer, Spacer)
info_menu.add_label("Defense Towers", label_id="towerDesc", max_char=-1, selectable=False, align=pygame_menu.locals.ALIGN_CENTER, font_size=20)

info_menu.add_label("Scout: Low DMG, High RNG, High SPD", label_id='ScoutT', max_char=-1, selectable=False, align=pygame_menu.locals.ALIGN_LEFT, margin=(0,8))
info_menu.add_label("Archer: Med DMG, Med RNG, Med SPD", label_id='ArcherT', max_char=-1, selectable=False, align=pygame_menu.locals.ALIGN_LEFT, margin=(0,8))
info_menu.add_label("Cannon: High DMG, Med RNG, Low SPD", label_id='CannonT', max_char=-1, selectable=False, align=pygame_menu.locals.ALIGN_LEFT, margin=(0,8))
info_menu.add_label("Ranger: Support only, buffs tower RNG", label_id='RangerT', max_char=-1, selectable=False, align=pygame_menu.locals.ALIGN_LEFT, margin=(0,8))
info_menu.add_label("Toughen: Support only, buffs tower DMG", label_id='ToughenT', max_char=-1, selectable=False, align=pygame_menu.locals.ALIGN_LEFT, margin=(0,8))

info_menu.add_vertical_margin(5)
info_menu.add_vertical_margin(5)
info_menu.add_vertical_margin(5)

################### COLUMN 3 ###################
info_menu.add_vertical_margin(35)
info_menu.add_image(os.path.join(ui_path, "EnemyList/Militia.png"), angle=0, image_id='MilitiaI', scale=(1,1), scale_smooth=True, selectable=False, align=pygame_menu.locals.ALIGN_RIGHT, margin=(0,5))
info_menu.add_image(os.path.join(ui_path, "EnemyList/Swordsman.png"), angle=0, image_id='SwordI', scale=(1,1), scale_smooth=True, selectable=False, align=pygame_menu.locals.ALIGN_RIGHT, margin=(0,5))
info_menu.add_image(os.path.join(ui_path, "EnemyList/LightCavalry.png"), angle=0, image_id='LightCavI', scale=(1,1), scale_smooth=True, selectable=False, align=pygame_menu.locals.ALIGN_RIGHT, margin=(0,5))
info_menu.add_image(os.path.join(ui_path, "EnemyList/Paladin.png"), angle=0, image_id='PaladinI', scale=(1,1), scale_smooth=True, selectable=False, align=pygame_menu.locals.ALIGN_RIGHT, margin=(0,5))
info_menu.add_image(os.path.join(ui_path, "EnemyList/Petard.png"), angle=0, image_id='PetardI', scale=(1,1), scale_smooth=True, selectable=False, align=pygame_menu.locals.ALIGN_RIGHT, margin=(0,5))

info_menu.add_vertical_margin(5)
info_menu.add_vertical_margin(5)
info_menu.add_vertical_margin(5)

################### COLUMN 4 ###################
info_menu.add_label("Enemies", label_id="enemyDesc", max_char=-1, selectable=False, align=pygame_menu.locals.ALIGN_CENTER, font_size=20)

info_menu.add_label("Militia: Basic enemy, low attack, armor, and health", label_id='MilitiaT', max_char=-1, selectable=False, align=pygame_menu.locals.ALIGN_LEFT, margin=(0,8))
info_menu.add_label("Swordsman: Higher armor and attack than Militia", label_id='SwordT', max_char=-1, selectable=False, align=pygame_menu.locals.ALIGN_LEFT, margin=(0,8))
info_menu.add_label("Light Cavalry: Horse rider with low armor and high speed", label_id='LightCavT', max_char=-1, selectable=False, align=pygame_menu.locals.ALIGN_LEFT, margin=(0,8))
info_menu.add_label("Paladin: Deadly armored knight on horseback", label_id='PaladinT', max_char=-1, selectable=False, align=pygame_menu.locals.ALIGN_LEFT, margin=(0,8))
info_menu.add_label("Petard: Slow moving, but deadly on impact to your castle", label_id='PetardT', max_char=-1, selectable=False, align=pygame_menu.locals.ALIGN_LEFT, margin=(0,8))

info_menu.add_vertical_margin(5)
info_menu.add_vertical_margin(150)

info_menu.add_button("BACK", action=returnToMenu, selection_effect=pygame_menu.widgets.HighlightSelection(border_width=1, margin_x=16.0, margin_y=8.0), align=pygame_menu.locals.ALIGN_CENTER, font_size=36)

################### COLUMN 5 ###################
info_menu.add_vertical_margin(35)
info_menu.add_image(os.path.join(ui_path, "Armor.png"), angle=0, image_id='ArmorI', scale=(1,1), scale_smooth=True, selectable=False, align=pygame_menu.locals.ALIGN_RIGHT, margin=(0,5))
info_menu.add_image(os.path.join(ui_path, "Attack.png"), angle=0, image_id='AttackI', scale=(1,1), scale_smooth=True, selectable=False, align=pygame_menu.locals.ALIGN_RIGHT, margin=(0,5))
info_menu.add_image(os.path.join(ui_path, "Range.png"), angle=0, image_id='RangeI', scale=(1,1), scale_smooth=True, selectable=False, align=pygame_menu.locals.ALIGN_RIGHT, margin=(0,5))
info_menu.add_image(os.path.join(ui_path, "Coins.png"), angle=0, image_id='CoinsI', scale=(1,1), scale_smooth=True, selectable=False, align=pygame_menu.locals.ALIGN_RIGHT, margin=(0,5))
info_menu.add_image(os.path.join(ui_path, "Build.png"), angle=0, image_id='BuildI', scale=(1,1), scale_smooth=True, selectable=False, align=pygame_menu.locals.ALIGN_RIGHT, margin=(0,5))
info_menu.add_image(os.path.join(ui_path, "Lives.png"), angle=0, image_id='LivesI', scale=(1,1), scale_smooth=True, selectable=False, align=pygame_menu.locals.ALIGN_RIGHT, margin=(0,5))
info_menu.add_image(os.path.join(ui_path, "Castle.png"), angle=0, image_id='CastleI', scale=(1,1), scale_smooth=True, selectable=False, align=pygame_menu.locals.ALIGN_RIGHT, margin=(0,5))

info_menu.add_vertical_margin(5)

################### COLUMN 6 ###################
info_menu.add_label("Game Attributes", label_id="attributeDesc", max_char=-1, selectable=False, align=pygame_menu.locals.ALIGN_CENTER, font_size=20)

info_menu.add_label("Armor: Represents the max health of an enemy", label_id='ArmorT', max_char=-1, selectable=False, align=pygame_menu.locals.ALIGN_LEFT, margin=(0,8))
info_menu.add_label("Attack: Represents the power of each enemy and tower", label_id='AttackT', max_char=-1, selectable=False, align=pygame_menu.locals.ALIGN_LEFT, margin=(0,8))
info_menu.add_label("Range: Reach of each tower to attack enemies", label_id='RangeT', max_char=-1, selectable=False, align=pygame_menu.locals.ALIGN_LEFT, margin=(0,8))
info_menu.add_label("Coins: Get from defeating enemies to build towers", label_id='CoinsT', max_char=-1, selectable=False, align=pygame_menu.locals.ALIGN_LEFT, margin=(0,8))
info_menu.add_label("Build: Create towers to defend your castle", label_id='BuildT', max_char=-1, selectable=False, align=pygame_menu.locals.ALIGN_LEFT, margin=(0,8))
info_menu.add_label("Lives: The health of your castle, game over at 0", label_id='LivesT', max_char=-1, selectable=False, align=pygame_menu.locals.ALIGN_LEFT, margin=(0,8))
info_menu.add_label("Castle: Your home, defend it at all costs", label_id='CastleT', max_char=-1, selectable=False, align=pygame_menu.locals.ALIGN_LEFT, margin=(0,8))

info_menu.add_vertical_margin(5)

def mainMenu(start_menu, info_menu):
    """
    Draws Main Menu to the screen
    Params: None
    Return: None?
    """
    pygame.mixer.music.stop()
    pygame.mixer.music.load(os.path.join("media/Music", "MainMenu.ogg"))
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1)
    
    while True:
        start_menu.enable()
        info_menu.disable()
    
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                quitter()
            
        if start_menu.is_enabled():
            start_menu.update(events)
            start_menu.draw(screen)
    
        # Only blits these images on main menu level 0
        if pygame_menu.Menu.get_current(start_menu) == start_menu:
            # Blit Rect for Castle Choice
            screen.blit(castle_imgs[castle_choice], (50, 325))
            # Blit Rect for Map Choice
            screen.blit(map_imgs[map_choice], (800, 325))
    
    
        pygame.mouse.set_visible(False)
        cursor_rect = pygame.mouse.get_pos()
        screen.blit(cursor_image, cursor_rect)
    
        pygame.display.update()

# Builds initial menu
mainMenu(start_menu, info_menu)