from pyo import *
import matplotlib.pyplot as plt
import pygame
from misc.pallete import *
import numpy as np

def pixels_to_small_float(val):
    val = val / 100.0
    if val < 0:
        val = 0
    if val > 1:
        val = 1

    return val

class Pin:
    def __init__(self, module, direction, position, parent, in_channel = 0):
        self.module = module
        self.dir = direction
        self.pos = position
        self.parent = parent
        self.in_channel = in_channel

    def draw(self, surface):
        pos = self.get_global_pos()
        pygame.draw.circle(surface, MODULE_PIN_COLOR, pos, 20)
        pygame.draw.circle(surface, MODULE_PIN_COLOR_INSIDE, pos, 10)

    def connect(self, pin):
        self.disconnect()
        self.module.addInput(self.in_channel, pin.module)
        self.module.setAmp(self.in_channel, 0, 1)

        # TODO: Other options. Change fixed pin 0
    
    def disconnect(self):
        self.module.delInput(self.in_channel)

    def get_global_pos(self):
        return (self.pos[0] + self.parent.pos[0], self.pos[1] + self.parent.pos[1])
    
class Potentiometer:
    def __init__(self, position, parent, default_value, min_value = 0, max_value=1):
        self.pos = position
        self.parent = parent
        self.val = default_value
        self.min_val = min_value
        self.max_val = max_value
        

    def draw(self, surface):
        pos = self.get_global_pos()
        pygame.draw.circle(surface, MODULE_PIN_COLOR, pos, 30)

        angle = np.interp(self.val, [self.min_val, self.max_val], [0, 2 * np.pi])

        line_length = 20
        end_x = pos[0] + line_length * np.cos(angle)
        end_y = pos[1] + line_length * np.sin(angle)

        pygame.draw.line(surface, (1, 1, 1), pos, (end_x, end_y), 2)

    def get_global_pos(self):
        return (self.pos[0] + self.parent.pos[0], self.pos[1] + self.parent.pos[1])

    def move(self, val, zero_val):
        self.val = float(np.interp(pixels_to_small_float(val - zero_val), [0, 1], [self.min_val, self.max_val]))


class ModuleBase:
    def __init__(self, pos, size):
        self.size = size
        self.pos = pos
        self.pins = []
        self.potentiometers = []
        self.name = "Base Module"
        self.font = pygame.font.SysFont('menlo', 24)
        
    def draw(self, surface):
        pygame.draw.rect(surface, MODULE_BASE_COLOR, pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1]))
        
        for i in range(len(self.pins)):
            self.pins[i].draw(surface)

        for i in range(len(self.potentiometers)):
            self.potentiometers[i].draw(surface)

    def check_clicks(self, pos):
        for i in range(len(self.pins)):
            pinpos = self.pins[i].get_global_pos()
            if np.abs(pos[0] - pinpos[0]) < 30 and np.abs(pos[1] - pinpos[1]) < 30:
                return self.pins[i]
            
        for i in range(len(self.potentiometers)):
            pinpos = self.potentiometers[i].get_global_pos()
            if np.abs(pos[0] - pinpos[0]) < 50 and np.abs(pos[1] - pinpos[1]) < 50:
                return self.potentiometers[i]

        return None
    
    def check_move(self, pos):
        if self.pos[0] < pos[0] < self.pos[0] + self.size[0] and self.pos[1] < pos[1] < self.pos[1] + self.size[1]:
            return True
        
        return False
    
    def get_relative_pos(self, pos):
        return (pos[0] - self.pos[0], pos[1] - self.pos[1])
    
    def update(self):
        pass

