from misc.pallete import *
import pygame

class MenuButton:
    """
    MenuButton defines a single button in the meny 
    """
    def __init__(self, size, pos, text):
        self.size = size
        self.pos = pos
        self.text = text
        self.font = pygame.font.SysFont('menlo', 24)

    def draw(self, surface):
        """
        draw draws the button

        args
            surface (Surface) - the main drawing surface
        """

        col = MODULE_BASE_COLOR

        # Check for hover over button and tint the color
        if self.click(pygame.mouse.get_pos()) != "":
            col = (col[0] * 0.9, col[1] * 0.9, col[2] * 0.9)

        pygame.draw.rect(surface, col, pygame.Rect(self.pos[0] - 5, self.pos[1] - 5, self.size[0], self.size[1]))
        text_surface = self.font.render(self.text, False, MODULE_PIN_COLOR_INSIDE)
        surface.blit(text_surface, self.pos)

    def click(self, pos):
        """
        click checks if button was clicked

        args
            pos (tuple) - pixel position of click

        returns
            (str) - the button text or empty string (if no click was found)
        """
        if self.pos[0] <= pos[0] <= self.pos[0] + self.size[0]  and self.pos[1] <= pos[1] <= self.pos[1] + self.size[1]:
            return self.text
        return ""

class Menu:
    """
    Menu defines the top menu bar for adding new modules
    """

    def __init__(self, window_width, window_height):
        self.font = pygame.font.SysFont('menlo', 24)
        self.width = window_width
        self.height = int(window_height / 20)

        self.buttons = [MenuButton((window_width / 10, self.height), (2 * window_width / 10, 0), "VCO"),
                        MenuButton((window_width / 10, self.height), (3 * window_width / 10, 0), "LFO"),
                        MenuButton((window_width / 10, self.height), (4 * window_width / 10, 0), "VCF"),
                        MenuButton((window_width / 10, self.height), (5 * window_width / 10, 0), "Mixer"),
                        MenuButton((window_width / 10, self.height), (6 * window_width / 10, 0), "Sequencer")]

    def draw(self, surface):
        """
        draw draws the menu

        args
            surface (Surface) - the main drawing surface
        """

        pygame.draw.rect(surface, MODULE_BASE_COLOR, pygame.Rect(0, 0, self.width, self.height))

        # Draw all buttons
        for i in range(len(self.buttons)):
            self.buttons[i].draw(surface)

        text_surface = self.font.render("Add module:", False, MODULE_PIN_COLOR_INSIDE)
        surface.blit(text_surface, (0, 0))

    def click(self, click_pos):
        """
        click checks clicks for all buttons

        args
            pos (tuple) - pixel position of click

        returns
            (str) - the clicked button text or empty string (if no click was found)
        """

        for i in range(len(self.buttons)):
            ret = self.buttons[i].click(click_pos)
            if ret != "":
                return ret

        return ""
    
class Tooltip:
    """
    Tooltips is a mouse tooltip when hovering over objects or clicking on potentiometers
    """
    def __init__(self):
        self.font = pygame.font.SysFont('menlo', 16)
        self.width = 70
        self.height = 30

    def draw(self, surface, mouse_pos, val):
        """
        draw draws the tooltip

        args
            surface (Surface) - the main drawing surface
            mouse_pos (tuple) - position of the mouse in pixels
            val (float) - tooltip value to display
        """

        w, h = self.font.size(val)
        pygame.draw.rect(surface, "black", pygame.Rect(mouse_pos[0] + 10, mouse_pos[1] + 10, w, h + 10))

        text_surface = self.font.render(val, False, "white")
        surface.blit(text_surface, (mouse_pos[0] + 10, mouse_pos[1] + 15))