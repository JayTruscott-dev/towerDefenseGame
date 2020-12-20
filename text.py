import pygame
pygame.init()

def display_text(msg, font, color, c_x, c_y):
    """
    Text displayer for messages to the user
    Params: msg (str): message to be displayed
            font (pygame.font.Font): font used for writing the message
            color (tuple): RGB list referencing the font color
            c_x (int): X coordinate value for the center of the blitting position
            c_y (int): Y coordinate value for the center of the blitting position
    Return: text_surf (pygame.Surface): new Surface containing the rendered text
            text_rect (tuple): new Rect of the surface position
    """
    text_surf, text_rect = text_objects(msg, font, color)
    text_rect.center = (c_x,c_y)
    
    return text_surf, text_rect

# This function generates the rectangle and surface used by display_text()
def text_objects(text, font, color):
    """
    This function is used to generate text objects used by text.display_text()
    Params: text (str): message to be rendered
            font (pygame.font.Font): font to render the message with
            color (tuple): RGB color list to render the message with
    Return: textSurface (pygame.Surface): new Surface containing the rendered text
            textSurface.get_rect() (tuple): new Rect containing the Surface positioning
    """
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()
