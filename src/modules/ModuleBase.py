from pyo import *
import matplotlib.pyplot as plt
import pygame
from misc.pallete import *
import numpy as np

class Pin:
    def __init__(self, module, direction, position, parent):
        self.module = module
        self.dir = direction
        self.pos = position
        self.parent = parent

    def draw(self, surface):
        pos = self.get_global_pos()
        pygame.draw.circle(surface, MODULE_PIN_COLOR, pos, 20)
        pygame.draw.circle(surface, MODULE_PIN_COLOR_INSIDE, pos, 10)

    def connect(self, pin):
        self.disconnect()
        self.module.addInput(0, pin.module)
        self.module.setAmp(0, 0, 1)

        # TODO: Other options. Change fixed pin 0
    
    def disconnect(self):
        self.module.delInput(0)

    def get_global_pos(self):
        return (self.pos[0] + self.parent.pos[0], self.pos[1] + self.parent.pos[1])


class ModuleBase:
    def __init__(self, pos, size):
        self.size = size
        self.pos = pos
        self.pins = []
        self.name = "Base Module"
        self.font = pygame.font.SysFont('menlo', 24)
        
    def draw(self, surface):
        pygame.draw.rect(surface, MODULE_BASE_COLOR, pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1]))
        
        for i in range(len(self.pins)):
            self.pins[i].draw(surface)

    def check_clicks(self, pos):
        for i in range(len(self.pins)):
            pinpos = self.pins[i].get_global_pos()
            if np.abs(pos[0] - pinpos[0]) < 50 and np.abs(pos[1] - pinpos[1]) < 50:
                return self.pins[i]
            
        return None
    
    def check_move(self, pos):
        if self.pos[0] < pos[0] < self.pos[0] + self.size[0] and self.pos[1] < pos[1] < self.pos[1] + self.size[1]:
            return True
        
        return False
    
    def get_relative_pos(self, pos):
        return (pos[0] - self.pos[0], pos[1] - self.pos[1])

