import pygame, os, math

class Map():
    def __init__(self):
        self.width = 1200
        self.height = 700
        self.path_locations = []
        self.path_corner_points = []
        self.castle_location = None
        self.bg = pygame.image.load(os.path.join("media/Backgrounds", "BG_BlankGrass.png"))
        #self.path_corners = [(0,80),(320,80),(320,500),(580,500),(580,260),(960,260),(960,400),(1100,400),(1200,400)]
        self.path_corners = []
        self.pathways = []
        
    def draw(self, screen):
        screen.blit(self.bg, (0,0))
        
    def getPathPoints(self):
        for i, p in enumerate(self.path_corners): # Enumerates through the corners list
            if i == len(self.path_corners) - 1:
                break
            elif i < len(self.path_corners) - 1:
                if p[0] < self.path_corners[i+1][0]: # Checks if the X at point p is < the X at point p+1
                # If this is true, increment the distance between X(p) and X(p+1) by 20
                # And append each increment to the pathways list
                    while p[0] != self.path_corners[i+1][0]:
                        self.pathways.append(p)
                        Y = p[1]
                        X = p[0] + 20
                        p = (X,Y)
                elif p[0] > self.path_corners[i+1][0]:
                    while p[0] != self.path_corners[i+1][0]:
                        self.pathways.append(p)
                        X = p[0] - 20
                        Y = p[1]
                        p = (X,Y)
                elif p[1] < self.path_corners[i+1][1]:
                    while p[1] != self.path_corners[i+1][1]:
                        self.pathways.append(p)
                        X = p[0]
                        Y = p[1] + 20
                        p = (X,Y)
                elif p[1] > self.path_corners[i+1][1]:
                    while p[1] != self.path_corners[i+1][1]:
                        self.pathways.append(p)
                        X = p[0]
                        Y = p[1] - 20
                        p = (X,Y)
            else:
                break
            
        return self.pathways