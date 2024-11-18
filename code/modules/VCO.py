from modules.ModuleBase import *

class VCO(ModuleBase):
    def __init__(self, pos):
        super().__init__(pos = pos, size=(200, 250))

        self.sine = Sine(440, mul = 1)
        self.pins.append(Pin(self.sine, "out", (self.pos[0] + self.size[0] - 25, self.pos[1] + 30)))
        self.name = "VCO"