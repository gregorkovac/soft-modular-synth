from modules.ModuleBase import *

class LFOModule(ModuleBase):
    def __init__(self, pos):
        super().__init__(pos = pos, size=(200, 260))

        self.osc = LFO(0.1, mul=1, add=0)
        self.pins.append(Pin("Out", self.osc, "out", (self.size[0] - 25, 30), self))
        
        self.potentiometers.append(Potentiometer("Shape", ( self.size[0] / 2, 100), self, 0.1, min_value=0.1, max_value=10))
        self.potentiometers.append(Potentiometer("Freq", (self.size[0] / 2, 200), self, 1, min_value=0, max_value=7.9))

        self.name = "LFO"

    def update(self):
        self.osc.type = int(np.floor(self.potentiometers[0].val))
        self.osc.freq = self.potentiometers[1].val

    def draw(self, surface):
        super().draw(surface)

        text_surface = self.font.render('LFO', False, TEXT_COLOR)
        surface.blit(text_surface, (self.pos[0] + self.size[0] / 2 - 25, self.pos[1] + 15))

        # pos = self.pins[0].get_global_pos()
        # text_surface = self.font.render('Out', False, TEXT_COLOR)
        # surface.blit(text_surface, (pos[0] - 25, pos[1] + 30))

        pos = self.potentiometers[0].get_global_pos()
        # text_surface = self.font.render('Shape', False, TEXT_COLOR)
        # surface.blit(text_surface, (pos[0] - 25, pos[1] + 30))

        pos = self.potentiometers[1].get_global_pos()
        # text_surface = self.font.render('Freq', False, TEXT_COLOR)
        # surface.blit(text_surface, (pos[0] - 25, pos[1] + 30))