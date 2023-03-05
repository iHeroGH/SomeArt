import pygame
from button import Button
from canvas import Canvas

class UI:

    def __init__(self):
        self.create_screen()
        self.create_toolbar_outline()
        self.create_toolbar()
        self.create_color_buttons()
        self.canvas = Canvas()

        self.refresh_screen()

        self.main_loop()

    def create_screen(self):
        self.screen = pygame.display.set_mode(size=(0, 0))
        self.screen.fill((255, 255, 255))
        pygame.display.set_caption("SomeArt")
    
    def create_toolbar_outline(self):
        self.toolbar_outline = pygame.Rect(0, 0, self.screen.get_size()[0]/10, self.screen.get_size()[1])
        pygame.draw.rect(self.screen, (0, 0, 0), self.toolbar_outline)
    
    def create_toolbar(self):
        self.toolbar = pygame.Rect(5, 5, self.screen.get_size()[0]/10-10, self.screen.get_size()[1]-10)
        pygame.draw.rect(self.screen, (255, 255, 255), self.toolbar)

    def create_color_buttons(self):
        self.color_button_size = self.toolbar.width - 20
        
        self.red_color_button = Button(15, 15, self.color_button_size, self.color_button_size)
        self.green_color_button = Button(15, self.red_color_button.topleft[1] + self.color_button_size + self.toolbar.height/10, self.color_button_size, self.color_button_size)
        self.blue_color_button = Button(15, self.green_color_button.topleft[1] + self.color_button_size + self.toolbar.height/10, self.color_button_size, self.color_button_size)
        self.black_color_button = Button(15, self.blue_color_button.topleft[1] + self.color_button_size + self.toolbar.height/10, self.color_button_size, self.color_button_size)
        
        pygame.draw.rect(self.screen, (255, 0, 0), self.red_color_button)
        pygame.draw.rect(self.screen, (0, 255, 0), self.green_color_button)
        pygame.draw.rect(self.screen, (0, 0, 255), self.blue_color_button)
        pygame.draw.rect(self.screen, (0, 0, 0), self.black_color_button)

    def refresh_screen(self):
        pygame.display.flip()

    def main_loop(self):
        self.is_running = True

        while self.is_running:
            for event in pygame.event.get():
                
                # PYGAME EVENTS
                if event.type == pygame.QUIT: # Top-Left X button (User Quits)
                    self.is_running = False

                # KEYBOARD EVENTS
                if event.type == pygame.KEYDOWN:

                    if event.key == 27: # Esc Key (User Quits)
                        self.is_running = False
                    
                    if event.key == 8: # Backspace Key (Reset Screen)
                        self.canvas.clear(self.screen, self.toolbar_outline)
                        self.refresh_screen()
                
                # MOUSE EVENTS
                # Mouse Motion
                if event.type == pygame.MOUSEMOTION:

                    if pygame.mouse.get_pressed(num_buttons=5)[0]: # Left Click (Draw as user moves)
                        position = pygame.mouse.get_pos()

                        if position[0] <= self.toolbar_outline.topright[0] + self.canvas.circle_size:
                            continue
                            
                        self.canvas.points_list.append(position)
                        self.canvas.draw(self.screen, (position[0], position[1]))
                        self.refresh_screen()
                    
                    self.canvas.fill_between_points(self.screen)
                
                # Mouse Press (Down)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    position = pygame.mouse.get_pos()

                    if event.button == 1: # Left Click (Draw as a user presses)
                        self.canvas.determine_color(self.red_color_button, self.green_color_button, self.blue_color_button, self.black_color_button)

                        if position[0] <= self.toolbar_outline.topright[0] + self.canvas.circle_size:
                            continue
                        
                        self.canvas.draw(self.screen, position)
                        self.refresh_screen()
                    
                    if event.button == 3: # Right click (Set color to white)
                        self.canvas.color = (255, 255, 255)

                # Mouse Press (Up)
                if event.type == pygame.MOUSEBUTTONUP:
                    
                    if event.button == 1: # Left Click Unpressed (Clear points list)
                        self.canvas.clear_points()
                    
                    # SCROLL WHEEL
                    if event.button == 4: # Scroll Up (Scale Up)
                        self.canvas.increase_circle_size()
                    
                    if event.button == 5: # Scroll Down (Scale Down)
                        self.canvas.decrease_circle_size()
                    

            
