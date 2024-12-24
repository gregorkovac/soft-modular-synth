from modules.ModuleBase import *

class VCF(ModuleBase):
    def __init__(self, pos):
        super().__init__(pos = pos, size=(200, 300))

        self.module = Tone(Sine(0, mul=0), freq = 440)

        self.pins.append(Pin("In", self.module, "pass", (25, 80), self, in_channel=0))
        self.pins.append(PinModifier("Freq", self.module, "in", (25, 150), self, "freq_filt"))
        self.pins.append(Pin("Out", self.module, "out", (self.size[0] - 25, self.size[1] / 2), self))

        self.potentiometers.append(Potentiometer("Freq", (self.size[0] / 2, 120), self, 400, min_value=0, max_value=5000))
        # self.potentiometers.append(Potentiometer("Res", (self.size[0] / 2, 220), self, 0, min_value=0, max_value=5))

        self.name = "VCF"

    def update(self):
        if self.pins[1].connected_to == None:
            self.module.freq = self.potentiometers[0].val
        # self.module.res = self.potentiometers[1].val

    def draw(self, surface):
        super().draw(surface)

        text_surface = self.font.render('VCF', False, TEXT_COLOR)
        surface.blit(text_surface, (self.pos[0] + 80, self.pos[1] + 15))

        # text_surface = self.font.render('Out', False, TEXT_COLOR)
        # surface.blit(text_surface, (self.pos[0] + self.size[0] - 50, self.pos[1] + self.size[1] / 2 + 15))