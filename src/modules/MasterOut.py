from modules.ModuleBase import *

class MasterOut(ModuleBase):
    def __init__(self, pos):
        super().__init__(pos = pos, size=(100, 100))

        self.module = Mixer(outs=1, chnls=1).out()
        self.pins.append(Pin(self.module, "in", (self.pos[0] + 25, self.pos[1] + 30)))

        self.name = "Master Out"