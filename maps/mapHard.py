import pygame
import os

from .map import Map

class MapHard(Map):
    def __init__(self):
        super().__init__()
        self.path_corners = [(0,0),(200,0),(200,320),(1000,320),(1000,660),(1200,660)]
    
    def draw(self, screen):
        super().draw(screen)
        
    # (0,00) - (200,0)    
    #              |   
    #          (200,300)    -->    (1000,300)
    #                                   |
    #                              (1000,400) --> (1200,400)
        
    
            