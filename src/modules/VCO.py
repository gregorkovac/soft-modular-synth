from modules.ModuleBase import *

class VCO(ModuleBase):
    """
    VCO serves as a basic sound generator
    """
    def __init__(self, pos):
        super().__init__(pos = pos, size=(200, 260))

        self.osc = Sine(440, mul = 1)
        
        # One output
        self.pins.append(Pin("Out", self.osc, "out", (self.size[0] - 25, 30), self))

        # Modifiers for amplitude and frequency
        self.pins.append(PinModifier("Amp", self.osc, "in", (25, 30), self, "mul"))
        self.pins.append(PinModifier("Freq", self.osc, "in", (25, 110), self, "freq"))

        # Potentiometer for frequency
        self.potentiometers.append(Potentiometer("Freq", (self.size[0] / 2, 120), self, 400, min_value=100, max_value=10000))

        self.name = "VCO"

    def update(self):
        """
        update updates the parameters based on potentiometers
        """

        if self.pins[2].connected_to == None:
            self.osc.freq = self.potentiometers[0].val
        elif isinstance(self.pins[2].connected_to.module, CustomConnection):
            self.osc.freq = self.pins[2].connected_to.module.value
        else:
            self.pins[2].connected_to.module.add = self.potentiometers[0].val

    def draw(self, surface):
        """
        draw draws the module

        args
            surface (Surface) - the main drawing surface
        """
        super().draw(surface)

        text_surface = self.font.render('VCO', False, TEXT_COLOR)
        surface.blit(text_surface, (self.pos[0] + self.size[0] / 2 - 25, self.pos[1] + 15))