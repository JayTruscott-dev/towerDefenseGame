import pygame
import os

pygame.font.init()

GOLDENROD   = (218,165, 32)

coins_big = pygame.transform.scale(pygame.image.load(os.path.join("menu", "Coins.png")), (50,50))
coins_small = pygame.transform.scale(pygame.image.load(os.path.join("menu", "Coins.png")), (20,20))
coins_xsmall = pygame.transform.scale(coins_small, (15,15))

onOff_bg = pygame.transform.scale(pygame.image.load(os.path.join("media/UserInterface", "no_icon.png")), (75,75))

font = pygame.font.Font("./fonts/Square.ttf", 24)
t_menu_font = pygame.font.Font("./fonts/Square.ttf", 12)

class Button:
    def __init__(self, menu, img, name):
        self.name = name
        self.img = img
        self.menu = menu
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.x = menu.x - self.width
        self.y = menu.y - self.height
        
    def click(self, X, Y):
        """
        This method handles if a user click collides with the menu
        Params: X (int): x coordinate of click
                Y (int): y coordinate of click
        Return: Bool
        """
        isClicked = False
        if X <= self.x + self.width and X >= self.x:
            if Y <= self.y + self.height and Y >= self.y:
                isClicked = True
        return isClicked
    
    def draw(self, screen):
        """
        This method draws the image for a button
        Params: screen (Surface): Pygame surface used for blitting
        Return: None
        """
        #upgrade_buffer_x = self.x + 3
        #upgrade_buffer_y = self.y + 1
        #sell_buffer_x = self.x + 55
        #sell_buffer_y = self.y + 1
        #if self.name == "Upgrade":
        #    screen.blit(self.img, (upgrade_buffer_x, upgrade_buffer_y))
        #elif self.name == "Sell":
        #    screen.blit(self.img, (sell_buffer_x, sell_buffer_y))
        #else:
        #    screen.blit(self.img, (self.x, self.y))
        screen.blit(self.img, (self.x, self.y))
        
    def update(self):
        """
        This method updates the position of the button
        Params: None
        Return: None
        """
        self.x = self.menu.x - 50
        self.y = self.menu.y - 110
        
        if self.name == "Upgrade":
            self.x += 3
            self.y += 1
        elif self.name == "Sell": # Actually gets clicked correctly now!!!!
            self.x += 55
            self.y += 1

class OnOffButton(Button):
    def __init__(self, play_img, pause_img, x, y):
        self.img = play_img
        self.play = play_img
        self.pause = pause_img
        self.x = x
        self.y = y
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.paused = True
    
    def draw(self, screen):
        """
        This method draws the paly/pause button to the menu
        Params: screen (Surface): Pygame surface used for blitting
        Return: None
        """
        if self.paused:
            screen.blit(onOff_bg, (self.x, self.y))
            screen.blit(self.play, (self.x, self.y))
        else:
            screen.blit(self.pause, (self.x, self.y))

class VerticalButton(Button):
    """
    Button class for each menu object
    Parent: Button class/object?
    """
    def __init__(self, x, y, img, name, cost):

        self.name = name
        self.x = x
        self.y = y
        self.img = img
        self.width = img.get_width()
        self.height = img.get_height()
        self.cost = cost


class Menu:
    """
    This class is used for building items
    """
    def __init__(self, tower, x, y, img, item_cost):
        self.x = x
        self.y = y
        self.width = img.get_width()
        self.height = img.get_height()
        self.item_cost = item_cost
        self.buttons = []
        self.items = 0
        self.bg = img
        #self.font = pygame.font.SysFont("helvetica", 18)
        self.font = t_menu_font
        self.tower = tower
    
    def add_btn(self, img, name):
        """
        This method is used to add each button to the menu
        Buttons include: Music, Play/Pause, Start Round, Build
        Params: img (Surface): Button surface used for blitting
                name (string): The name of the button
        Return: None
        """
        self.items += 1
        self.buttons.append(Button(self, img, name))
        
    def get_item_cost(self):
        """
        This method retrieves the item cost of a selected tower button (to upgrade)
        Params: None
        Return: item_cost (int): cost to upgrade
        """
        return self.item_cost[self.tower.level - 1]
    
    #def get_sell_price(self):
    #    price = self.item_cost[self.tower.level - 1] / 2
    #    return price
    
    def draw(self, screen):
        """
        This method draws the in-game menu to the screen
        Params: screen (Surface): game surface
        Return: None
        """
        loc_x = self.x - self.bg.get_width()/2
        loc_y = self.y - 120
        screen.blit(self.bg, (loc_x, loc_y))
        for item in self.buttons:
            item.draw(screen)
            #item_margin_x = item.x + item.width + 5
            #item_margin_y = item.y - 9
            # BLITTER (COINS IMAGE)
            #item_margin_x = loc_x + 13
            #item_margin_y = self.bg.get_height()
            #screen.blit(coins_xsmall, (item.x + item.width/2 - 4, item.y + coins_xsmall.get_height() + 20))
            # BLITTER (ITEM COST)
            if item.name == "Upgrade":
                text = self.font.render(str(self.item_cost[self.tower.level - 1]), 1, (255,255,255))
            elif item.name == "Sell":
                text = self.font.render(str(int(self.tower.price[self.tower.level - 1] / 2)), 1, (255,255,255))
            screen.blit(text, (item.x + item.width/2 - text.get_width()/2 + 1, item.y + coins_xsmall.get_height() + 20))
    
    def get_clicked(self, X, Y):
        """
        This method retrieves the clicked item from the menu
        Params: X (int): x coordinate of the click
                Y (int): y coordinate of the click
        Return: Button name if the click interacted with a button, else returns None
        """
        for btn in self.buttons:
            if btn.click(X,Y):
                return btn.name
            
        return None
    
    def update(self):
        """
        This method updates the menu with the button location
        Params: None
        Return: None
        """
        for btn in self.buttons:
            btn.update()


class VerticalMenu(Menu):
    """
    This class is used to build the vertical sidebar for the game
    """
    def __init__(self, x, y, img):
        self.x = x # screen.width - side_ui.get_width() + 70 = 1200 - 110 + 70 = 1160
        self.y = y # 250
        self.width = img.get_width()
        self.height = img.get_height()
        self.buttons = []
        self.items = 0
        self.bg = img
        self.font = font
        #self.font = pygame.font.SysFont("helvetica", 18)
    
    def add_btn(self, img, name, cost):
        """
        This method is used for adding buttons to the menu
        Params: img (Surface): surface used for blitting the button image
                name (str): button identifier
                cost (int): buy cost for a tower
        Return: None
        """
        self.items += 1
        btn_x = self.x - 40
        btn_y = self.y - 150 + (self.items-1)*100
        self.buttons.append(VerticalButton(btn_x, btn_y, img, name, cost))
        
    def get_item_cost(self, name):
        """
        This method is used for retrieving the cost for buying a new tower
        Params: name (str): Tower identifier
        Return: cost (int): Tower cost, or -1 if no tower matches the identifier
        """
        for btn in self.buttons:
            if btn.name == name:
                return btn.cost
        return -1
    
    def draw(self, screen):
        """
        This method is used for drawing the menu buttons and its background to the screen
        Params: screen (Surface): surface used for blitting
        Return: None
        """
        ui_bg = pygame.Surface((110,700), pygame.SRCALPHA, 32)
        ui_bg.fill((95,52,9,200))
        screen.blit(ui_bg, (1090,0))
        
        for item in self.buttons:
            item.draw(screen)
            screen.blit(coins_small, (item.x - 10, item.y + item.height + 10))
            text = self.font.render(str(item.cost), 1, GOLDENROD)
            screen.blit(text, (item.x + item.width/2 - text.get_width()/2 + 17, item.y + item.height + 10))
            