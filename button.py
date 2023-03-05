import pygame

class Button(pygame.Rect):
    """Button class is a subclass of the Pygame Rect class, adding a method to check if the mouse is hovering over the rect
    
    Attributes:
        left (float): The coordinate of the left point of the rectangle
        top (float): The coordinate of the top point of the rectangle
        width (float): The width of the rectangle
        height (float): The height of the rectangle

    """

    def __init__(self, left: float, top: float, width: float, height: float) -> None:
        """Simply calls the super class's init function
        
        Args:
            left (float): The coordinate of the left point of the rectangle
            top (float): The coordinate of the top point of the rectangle
            width (float): The width of the rectangle
            height (float): The height of the rectangle
        
        Returns:
            None

        """
        super().__init__(left, top, width, height)
    
    def is_hovering(self) -> bool:
        """Returns whether or not the mouse is hovering over the button
        
        Returns:
            is_hover (bool): Whether or not the mouse is hovering over the button

        """
        position = pygame.mouse.get_pos()
        # Return True if the x position is within the left and right bound and if the y position is within the top and bottom bound
        return (self.left <= position[0] <= self.width + self.left) and (self.top <= position[1] <= self.top + self.height)