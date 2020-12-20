import pygame
import os

from .map import Map

class MapEasy(Map):
    def __init__(self):
        super().__init__()
        self.path_corners = [(0,80),(320,80),(320,500),(580,500),(580,260),(960,260),(960,400),(1100,400),(1200,400)]
    
    def draw(self, screen):
        super().draw(screen)
        
    # (0,80) - (320,80)    (580,260) - (960,260)
    #              |           |           |
    #          (320,500) - (580,500)   (960,400) - (1100,400) - (1200,400)
        
    
            