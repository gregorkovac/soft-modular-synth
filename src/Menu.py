from misc.pallete import *
import pygame

class MenuButton:
    def __init__(self, width, height, pos, text):
        self.width = width
        self.height = height
        self.pos = pos
        self.text = text
        self.font = pygame.font.SysFont('menlo', 24)

    def draw(self, surface):
        col = MODULE_BASE_COLOR
        if self.click(pygame.mouse.get_pos()) != "":
            col = (col[0] * 0.9, col[1] * 0.9, col[2] * 0.9)

        pygame.draw.rect(surface, col, pygame.Rect(self.pos[0] - 5, self.pos[1] - 5, self.width, self.height))
        text_surface = self.font.render(self.text, False, MODULE_PIN_COLOR_INSIDE)
        surface.blit(text_surface, self.pos)

    def click(self, pos):
        if self.pos[0] <= pos[0] <= self.pos[0] + self.width  and self.pos[1] <= pos[1] <= self.pos[1] + self.height:
            return self.text
        return ""

class Menu:
    def __init__(self, window_width, window_height):
        self.font = pygame.font.SysFont('menlo', 24)
        self.width = window_width
        self.height = int(window_height / 20)

        self.buttons = [MenuButton(window_width / 10, self.height, (2 * window_width / 10, 0), "VCO"),
                        MenuButton(window_width / 10, self.height, (3 * window_width / 10, 0), "LFO"),
                        MenuButton(window_width / 10, self.height, (4 * window_width / 10, 0), "VCF"),
                        MenuButton(window_width / 10, self.height, (5 * window_width / 10, 0), "Mixer")]

    def draw(self, surface):
        pygame.draw.rect(surface, MODULE_BASE_COLOR, pygame.Rect(0, 0, self.width, self.height))

        for i in range(len(self.buttons)):
            self.buttons[i].draw(surface)

        text_surface = self.font.render("Add module:", False, MODULE_PIN_COLOR_INSIDE)
        surface.blit(text_surface, (0, 0))

    def click(self, click_pos):
        for i in range(len(self.buttons)):
            ret = self.buttons[i].click(click_pos)
            if ret != "":
                return ret

        return ""
    
class Tooltip:
    def __init__(self):
        self.font = pygame.font.SysFont('menlo', 16)
        self.width = 70
        self.height = 30

    def draw(self, surface, mouse_pos, val):
        val = str(round(val, 1))

        pygame.draw.rect(surface, "black", pygame.Rect(mouse_pos[0] + 10, mouse_pos[1] + 10, self.width, self.height))
        text_surface = self.font.render(val, False, "white")
        surface.blit(text_surface, (mouse_pos[0] + 10, mouse_pos[1] + 15))