import pygame

from button import Button
from canvas import Canvas

class UI:
    """UI Class holds everything necessary to set up the user interface and translates inputs into commands for the canvas"""

    def __init__(self) -> None:
        """Initializes the user interface by delegating the different aspects of the screen to other functions"""
        self.create_screen() # Initialize the pygame surface
        self.create_toolbar_outline() # Create the toolbar outline to host the toolbar 
        self.create_toolbar() # Create the toolbar to host the color buttons
        self.create_color_buttons() # Create the color buttons
        self.canvas = Canvas() # Create a canvas object

        self.refresh_screen() # Refresh the screen to display everything created

        self.main_loop() # Begin the main loop

    def create_screen(self) -> None:
        """Initializes the Pygame surface to a size of (0,0), which spans the entire device's screen"""
        self.screen = pygame.display.set_mode(size=(0, 0))
        self.screen.fill((255, 255, 255)) # Start with a completely white canvas
        pygame.display.set_caption("SomeArt")
    
    def create_toolbar_outline(self) -> None:
        """Creates the toolbar outline and draws it to the screen"""
        self.toolbar_outline = pygame.Rect(0, 0, self.screen.get_size()[0]/10, self.screen.get_size()[1])
        pygame.draw.rect(self.screen, (0, 0, 0), self.toolbar_outline)
    
    def create_toolbar(self) -> None:
        """Creates the toolbar itself and draws it to the screen"""
        self.toolbar = pygame.Rect(5, 5, self.screen.get_size()[0]/10-10, self.screen.get_size()[1]-10)
        pygame.draw.rect(self.screen, (255, 255, 255), self.toolbar)

    def create_color_buttons(self) -> None:
        """Create the buttons for the 4 color options
        
        First, we initialize a size for the color button which is dependent on the width of the toolbar.
        Next, we create a Button for each of the red, green, blue, and black color options

        """
        # The size of a color button
        self.color_button_size = self.toolbar.width - 20
        
        # Create the 4 button objects
        self.red_color_button = Button(15, 15, self.color_button_size, self.color_button_size)
        self.green_color_button = Button(15, self.red_color_button.topleft[1] + self.color_button_size + self.toolbar.height/10, self.color_button_size, self.color_button_size)
        self.blue_color_button = Button(15, self.green_color_button.topleft[1] + self.color_button_size + self.toolbar.height/10, self.color_button_size, self.color_button_size)
        self.black_color_button = Button(15, self.blue_color_button.topleft[1] + self.color_button_size + self.toolbar.height/10, self.color_button_size, self.color_button_size)
        
        # Draw the 4 button objects
        pygame.draw.rect(self.screen, (255, 0, 0), self.red_color_button)
        pygame.draw.rect(self.screen, (0, 255, 0), self.green_color_button)
        pygame.draw.rect(self.screen, (0, 0, 255), self.blue_color_button)
        pygame.draw.rect(self.screen, (0, 0, 0), self.black_color_button)

    def refresh_screen(self) -> None:
        """Call the pygame.display.flip() function to refresh the screen to reflect new changes"""
        pygame.display.flip()

    def main_loop(self) -> None:
        """Keep users in the input loop until they exit the program"""
        
        # Keep track of if a user quits
        self.is_running = True

        while self.is_running:
            # Loop through all the Pygame events
            for event in pygame.event.get():
                
                # PYGAME EVENTS
                if event.type == pygame.QUIT: # Top-Left X button (User Quits)
                    self.is_running = False

                # KEYBOARD EVENTS
                # A key is pressed
                if event.type == pygame.KEYDOWN:

                    if event.key == 27: # Esc Key (User Quits)
                        self.is_running = False # Exit out of the loop
                    
                    if event.key == 8: # Backspace Key (Reset Screen)
                        self.canvas.clear(self.screen, self.toolbar_outline) # Clear the canvas
                        self.refresh_screen()
                
                # MOUSE EVENTS
                # Mouse Motion
                if event.type == pygame.MOUSEMOTION:

                    if pygame.mouse.get_pressed(num_buttons=5)[0]: # Left Click (Draw as user moves)
                        position = pygame.mouse.get_pos() # Get the position of the mouse

                        # Make sure we're in bounds of the canvas
                        if not self.canvas.in_bounds(position, self.toolbar_outline):
                            continue
                        
                        # Since we're moving, add the position to the points list and draw a circle at the positions we move through
                        self.canvas.points_list.append(position)
                        self.canvas.draw(self.screen, (position[0], position[1]))

                        # Refresh the screen
                        self.refresh_screen()
                    
                    # Since we may have created a points_list, draw a line between each pair of points
                    self.canvas.fill_between_points(self.screen)
                
                # Mouse Press (Down)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    position = pygame.mouse.get_pos() # Get the mouse position

                    if event.button == 1: # Left Click (Draw as a user presses)
                        # If we're over a color button, choose the color
                        self.canvas.determine_color(self.red_color_button, self.green_color_button, self.blue_color_button, self.black_color_button)

                        # Check if we're within the bounds of the canvas
                        if not self.canvas.in_bounds(position, self.toolbar_outline):
                            continue
                        
                        # Draw a point at the current position (since we aren't moving the mouse)
                        self.canvas.draw(self.screen, position)

                        # Refresh the screen
                        self.refresh_screen()
                    
                    if event.button == 3: # Right click (Set color to white)
                        self.canvas.color = (255, 255, 255)

                # Mouse Press (Up)
                if event.type == pygame.MOUSEBUTTONUP:
                    
                    if event.button == 1: # Left Click Unpressed (Clear points list)
                        # When we release the left button, clear the points list
                        self.canvas.clear_points()
                    
                    # SCROLL WHEEL
                    if event.button == 4: # Scroll Up (Scale Up)
                        self.canvas.increase_circle_size()
                    
                    if event.button == 5: # Scroll Down (Scale Down)
                        self.canvas.decrease_circle_size()
                    

            
