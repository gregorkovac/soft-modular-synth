from pyo import *
import matplotlib.pyplot as plt
import pygame
from misc.pallete import *
import numpy as np

class Pin:
    def __init__(self, module, direction, position):
        self.module = module
        self.dir = direction
        self.pos = position

    def draw(self, surface):
        pygame.draw.circle(surface, MODULE_PIN_COLOR, self.pos, 20)
        pygame.draw.circle(surface, (0, 0, 0), self.pos, 10)

    def connect(self, pin):
        self.disconnect()
        self.module.addInput(0, pin.module)
        self.module.setAmp(0, 0, 1)

        # TODO: Other options. Change fixed pin 0
    
    def disconnect(self):
        self.module.delInput(0)


class ModuleBase:
    def __init__(self, pos, size):
        self.size = size
        self.pos = pos
        self.pins = []
        self.name = "Base Module"
        
    def draw(self, surface):
        pygame.draw.rect(surface, MODULE_BASE_COLOR, pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1]))
        
        for i in range(len(self.pins)):
            self.pins[i].draw(surface)

    def check_clicks(self, pos):
        print("----")
        print(self.name)
        for i in range(len(self.pins)):
            print(f"{pos} vs. {self.pins[i].pos}")
            if np.abs(pos[0] - self.pins[i].pos[0]) < 50 and np.abs(pos[1] - self.pins[i].pos[1]) < 50:
                return self.pins[i]
            
        return None

