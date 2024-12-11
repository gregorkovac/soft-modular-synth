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
        pygame.draw.rect(surface, TEXT_COLOR, pygame.Rect(self.pos[0] - 5, self.pos[1] - 5, self.width, self.height))
        text_surface = self.font.render(self.text, False, MODULE_PIN_COLOR_INSIDE)
        surface.blit(text_surface, self.pos)

    def click(self, pos):
        if self.pos[0] <= pos[0] <= self.pos[0] + self.width  and self.pos[1] <= pos[1] <= self.pos[1] + self.height:
            return self.text
        return ""

class Menu:
    def __init__(self, window_width, window_height):
        self.width = window_width
        self.height = int(window_height / 20)

        self.buttons = [MenuButton(window_width / 20, self.height * 2/3, (20, self.height / 5), "VCO"),
                        MenuButton(window_width / 20, self.height * 2/3, (120, self.height / 5), "LFO"),
                        MenuButton(window_width / 10, self.height * 2/3, (220, self.height / 5), "Mixer")]

    def draw(self, surface):
        pygame.draw.rect(surface, MODULE_BASE_COLOR, pygame.Rect(0, 0, self.width, self.height))

        for i in range(len(self.buttons)):
            self.buttons[i].draw(surface)

    def click(self, click_pos):
        for i in range(len(self.buttons)):
            ret = self.buttons[i].click(click_pos)
            if ret != "":
                return ret

        return ""