from modules.ModuleBase import *

class Mix(ModuleBase):
    def __init__(self, pos):
        super().__init__(pos = pos, size=(200, 340))

        self.module = Mixer(outs=1, chnls=4)
        self.pins.append(Pin(self.module, "in", (25, 80), self, in_channel=0))
        self.pins.append(Pin(self.module, "in", (25, 150), self, in_channel=1))
        self.pins.append(Pin(self.module, "in", (25, 220), self, in_channel=2))
        self.pins.append(Pin(self.module, "in", (25, 290), self, in_channel=3))

        self.pins.append(Pin(self.module[0], "out", (self.size[0] - 25, self.size[1] / 2), self))

        self.potentiometers.append(Potentiometer((80, 80), self, 1, min_value=0, max_value=1))
        self.potentiometers.append(Potentiometer((80, 150), self, 1, min_value=0, max_value=1))
        self.potentiometers.append(Potentiometer((80, 220), self, 1, min_value=0, max_value=1))
        self.potentiometers.append(Potentiometer((80, 290), self, 1, min_value=0, max_value=1))

        self.name = "Mixer"

    def update(self):
        self.module.setAmp(0, 0, self.potentiometers[0].val)
        self.module.setAmp(1, 0, self.potentiometers[1].val)
        self.module.setAmp(2, 0, self.potentiometers[2].val)
        self.module.setAmp(3, 0, self.potentiometers[3].val)

    def draw(self, surface):
        super().draw(surface)

        text_surface = self.font.render('MIXER', False, TEXT_COLOR)
        surface.blit(text_surface, (self.pos[0] + 60, self.pos[1] + 15))

        text_surface = self.font.render('Out', False, TEXT_COLOR)
        surface.blit(text_surface, (self.pos[0] + self.size[0] - 50, self.pos[1] + self.size[1] / 2 + 15))