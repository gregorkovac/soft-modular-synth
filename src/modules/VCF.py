from modules.ModuleBase import *

class VCF(ModuleBase):
    """
    VCF serves as low pass filter 
    """

    def __init__(self, pos):
        super().__init__(pos = pos, size=(200, 300))

        self.module = Tone(Sine(0, mul=0), freq = 440)

        # One input
        self.pins.append(Pin("In", self.module, "pass", (25, 80), self, in_channel=0))

        # One modifier pin for frequency
        self.pins.append(PinModifier("Freq", self.module, "in", (25, 150), self, "freq_filt"))

        # One output
        self.pins.append(Pin("Out", self.module, "out", (self.size[0] - 25, self.size[1] / 2), self))

        # One potentiometer for frequency
        self.potentiometers.append(Potentiometer("Freq", (self.size[0] / 2, 120), self, 400, min_value=0, max_value=5000))

        self.name = "VCF"

    def update(self):
        """
        update updates the parameters based on potentiometers
        """
        if self.pins[1].connected_to == None:
            self.module.freq = self.potentiometers[0].val

    def draw(self, surface):
        """
        draw draws the module

        args
            surface (Surface) - the main drawing surface
        """
        super().draw(surface)

        text_surface = self.font.render('VCF', False, TEXT_COLOR)
        surface.blit(text_surface, (self.pos[0] + 80, self.pos[1] + 15))