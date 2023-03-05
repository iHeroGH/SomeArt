import pygame

class Button(pygame.Rect):

    def __init__(self, left, top, width, height):
        super().__init__(left, top, width, height)
    
    def is_pressed(self):
        position = pygame.mouse.get_pos()
        return (self.left <= position[0] <= self.width + self.left) and (self.top <= position[1] <= self.top + self.height)