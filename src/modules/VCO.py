from modules.ModuleBase import *

class VCO(ModuleBase):
    def __init__(self, pos):
        super().__init__(pos = pos, size=(200, 250))

        self.osc = Sine(440, mul = 1)
        self.pins.append(Pin("Out", self.osc, "out", (self.size[0] - 25, 30), self))
        self.pins.append(PinModifier("Amp", self.osc, "in", (25, 30), self, "mul"))
        self.pins.append(PinModifier("Freq", self.osc, "in", (25, 110), self, "freq"))

        self.potentiometers.append(Potentiometer("Freq", (self.size[0] / 2, 120), self, 400, min_value=100, max_value=2000))
        
        self.name = "VCO"

    def update(self):
        if self.pins[2].connected_to == None:
            self.osc.freq = self.potentiometers[0].val
        else:
            self.pins[2].connected_to.module.add = self.potentiometers[0].val

    def draw(self, surface):
        super().draw(surface)

        text_surface = self.font.render('VCO', False, TEXT_COLOR)
        surface.blit(text_surface, (self.pos[0] + self.size[0] / 2 - 25, self.pos[1] + 15))

        # pos = self.pins[0].get_global_pos()
        # text_surface = self.font.render('Out', False, TEXT_COLOR)
        # surface.blit(text_surface, (pos[0] - 25, pos[1] + 30))

        # pos = self.pins[1].get_global_pos()
        # text_surface = self.font.render('Amp', False, TEXT_COLOR)
        # surface.blit(text_surface, (pos[0] - 20, pos[1] + 30))

        # pos = self.pins[2].get_global_pos()
        # text_surface = self.font.render('Freq', False, TEXT_COLOR)
        # surface.blit(text_surface, (pos[0] - 20, pos[1] + 30))

        # pos = self.potentiometers[0].get_global_pos()
        # text_surface = self.font.render('Freq', False, TEXT_COLOR)
        # surface.blit(text_surface, (pos[0] - 25, pos[1] + 30))