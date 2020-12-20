import pygame
import os

from .map import Map

class MapMedium(Map):
    def __init__(self):
        super().__init__()
        self.path_corners = [(0,80),(500,80),(500,500),(300,500),(300,660),(1100,660),(1200,660)]
    
    def draw(self, screen):
        super().draw(screen)
        
    # (0,80)    -->     (500,80)
    #                       |
    #     (300,500) <-- (500,500)
    #         |
    #     (300,660)           -->        (1100,660) --> (1200,660)
    
            