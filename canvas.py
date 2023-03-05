import pygame
from pygame import gfxdraw

from button import Button

class Canvas:

    def __init__(self):
        self.circle_size = 10
        self.color = (0, 0, 0)
        self.points_list = []
    
    def draw(self, screen, position):
        gfxdraw.aacircle(screen, position[0], position[1], self.circle_size, self.color)
        gfxdraw.filled_circle(screen, position[0], position[1], self.circle_size, self.color)

    def fill_between_points(self, screen):
        for n, point in enumerate(self.points_list):
            try:
                gfxdraw.aacircle(screen, point[0], point[1], self.circle_size, self.color)
                gfxdraw.filled_circle(screen, point[0], point[1], self.circle_size, self.color)
                pygame.draw.line(screen, self.color, point, self.points_list[1], self.circle_size * 2 - 1)
                self.points_list.pop(n)
            except IndexError:
                pass

    def determine_color(
            self, red_color_button: Button, green_color_button: Button, blue_color_button: Button, black_color_button: Button
            ):
        
        if red_color_button.is_pressed(): self.color = (255, 0, 0)
        if green_color_button.is_pressed(): self.color = (0, 255, 0)
        if blue_color_button.is_pressed(): self.color = (0, 0, 255)
        if black_color_button.is_pressed(): self.color = (0, 0, 0)

    def increase_circle_size(self):
        self.circle_size = min(self.circle_size + 5, 50)

    def decrease_circle_size(self):
        self.circle_size = max(self.circle_size - 5, 1)

    def clear_points(self):
        self.points_list = []

    def clear(self, screen, toolbar_outline):
        white_square = pygame.Rect(toolbar_outline.topright[0], 0, screen.get_size()[0]+toolbar_outline.width, screen.get_size()[1])
        pygame.draw.rect(screen, (255, 255, 255), white_square)