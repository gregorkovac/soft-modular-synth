from modules.ModuleBase import *

class LFOModule(ModuleBase):
    """
    LFOModule is a low frequency oscillator that is primarily used for controlling parameters
    """
    def __init__(self, pos):
        super().__init__(pos = pos, size=(200, 260))

        self.osc = LFO(0.1, mul=1, add=0)

        # The module has one output pin
        self.pins.append(Pin("Out", self.osc, "out", (self.size[0] - 25, 30), self))
        
        # The module has two inputs - shape and frequency
        self.potentiometers.append(Potentiometer("Shape", ( self.size[0] / 2, 100), self, 0.1, min_value=0.1, max_value=10))
        self.potentiometers.append(Potentiometer("Freq", (self.size[0] / 2, 200), self, 1, min_value=0, max_value=7.9))

        self.name = "LFO"

    def update(self):
        """
        update updates the parameters based on potentiometers
        """
        
        self.osc.type = int(np.floor(self.potentiometers[0].val))
        self.osc.freq = self.potentiometers[1].val

    def draw(self, surface):
        """
        draw draws the module

        args
            surface (Surface) - the main drawing surface
        """

        super().draw(surface)

        text_surface = self.font.render('LFO', False, TEXT_COLOR)
        surface.blit(text_surface, (self.pos[0] + self.size[0] / 2 - 25, self.pos[1] + 15))