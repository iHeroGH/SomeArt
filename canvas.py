import pygame
from pygame import gfxdraw

from button import Button

class Canvas:
    """Canvas class holds everything necessary to draw to the screen

    Attributes:
        circle_size (int): The radius of the circle
        color (tuple): A tuple representing the (R, G, B) values of a color. The current color selected
        points_list (list[tuple]): A list of tuples of the positions of the points between the drawn circles

    """

    def __init__(self) -> None:
        """Sets the default values for the attributes
        
        Sets the circle_size to its default value (10), the default color to its default color (black), and the points_list to an empty list
        
        """
        self.circle_size: int = 10
        self.color: tuple = (0, 0, 0)
        self.points_list: list[tuple] = []
    
    def draw(self, screen: pygame.Surface, position: tuple) -> None:
        """Draws a single circle to the screen

        Draws an antialiased circle to the screen at the given position

        Args:
            screen (pygame.Surface): The surface to draw the circle onto
            position (tuple): The position to draw the circle at
        """
        gfxdraw.aacircle(screen, position[0], position[1], self.circle_size, self.color)
        gfxdraw.filled_circle(screen, position[0], position[1], self.circle_size, self.color)

    def fill_between_points(self, screen: pygame.Surface) -> None:
        """Draws circles and lines between the points pressed (to prevent cracking)

        Draws an antialiased circle at the points passed, and follows it with a line to maintain a solid shape

        Args:
            screen (pygame.Surface): The surface to draw the shapes onto 

        """
        # Loop through each point
        for n, point in enumerate(self.points_list):
            try:
                # Draw the anti-aliased border and the filled shape at the current point
                gfxdraw.aacircle(screen, point[0], point[1], self.circle_size, self.color)
                gfxdraw.filled_circle(screen, point[0], point[1], self.circle_size, self.color)
                # Fill the space between the current point and the next point with a line
                pygame.draw.line(screen, self.color, point, self.points_list[1], self.circle_size * 2 - 1)
                # Remove the current point
                self.points_list.pop(n)
            except IndexError:
                pass
            
    def determine_color(
            self, red_color_button: Button, green_color_button: Button, blue_color_button: Button, black_color_button: Button
            ) -> None:
        """Determines what color to use

        Checks for if the mouse is hovering over any of the color buttons and changes the color accordingly

        Args:
            red_color_button (Button): The button for the red color
            green_color_button (Button): The button for the green color
            blue_color_button (Button): The button for the blue color
            black_color_button (Button): The button for the black color

        """
        
        if red_color_button.is_hovering(): self.color = (255, 0, 0) # If the red color is hovered, change the color to red
        if green_color_button.is_hovering(): self.color = (0, 255, 0) # If the green color is hovered, change the color to green
        if blue_color_button.is_hovering(): self.color = (0, 0, 255) # If the blue color is hovered, change the color to blue
        if black_color_button.is_hovering(): self.color = (0, 0, 0) # If the black color is hovered, change the color to black

    def increase_circle_size(self) -> None:
        """Increases the radius of the circle by 5 (to a maximum of 50)"""
        self.circle_size = min(self.circle_size + 5, 50)

    def decrease_circle_size(self) -> None:
        """Decreases the radius of the circle by 5 (to a minimum of 0)"""
        self.circle_size = max(self.circle_size - 5, 1)

    def clear_points(self) -> None:
        """Clear the list of points (points_list)"""
        self.points_list = []

    def clear(self, screen: pygame.Surface, toolbar_outline: pygame.Rect) -> None:
        """Clear the screen of any drawing
        
        Creates a white square and fills the canvas with it
        
        Args:
            screen (pygame.Surface): The surface to clear
            toolbar_outline (pygame.Rect): The toolbar outline to make sure we only clear the canvas and not the toolbar itself

        """
        # Create the white square to cover the canvas (starting from the toolbar outline)
        white_square = pygame.Rect(toolbar_outline.topright[0], 0, screen.get_size()[0]+toolbar_outline.width, screen.get_size()[1])
        # Draw the square
        pygame.draw.rect(screen, (255, 255, 255), white_square)
    
    def in_bounds(self, position: tuple, toolbar_outline: pygame.Rect) -> bool:
        """Return whether or not we are in bounds with the canvas (without interfering with the toolbar)

        Args:
            position (tuple): The current position of the mouse
            toolbar_outline (pygame.Rect): The outline of the toolbar (to make sure we aren't interfering with it)
        """
        # Return True if the x coordinate is beyond the toolbar outline (taking into account the circle radius)
        return position[0] >= toolbar_outline.topright[0] + self.circle_size