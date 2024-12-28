from modules.ModuleBase import *

class VCF(ModuleBase):
    """
    VCF serves as low pass filter 
    """

    def __init__(self, pos):
        super().__init__(pos = pos, size=(200, 300))

        self.module = MoogLP(Sine(0, mul=0), freq = 440, res=1.25)

        # One input
        self.pins.append(Pin("In", self.module, "pass", (25, 80), self, in_channel=0,
                             tooltip="I take in a signal"))

        # One modifier pin for frequency
        self.pins.append(PinModifier("Freq", self.module, "in", (25, 150), self, "freq_filt",
                                     tooltip="I control how muffled the output is based on the input signal"))

        # One output
        self.pins.append(Pin("Out", self.module, "out", (self.size[0] - 25, self.size[1] / 2), self,
                             tooltip="I output a muffled signal"))

        # One potentiometer for frequency
        self.potentiometers.append(Potentiometer("Freq", (self.size[0] / 2, 120), self, 400, min_value=0, max_value=5000,
                                                 tooltip="I manually control how muffled the output is"))
        
        self.potentiometers.append(Potentiometer("Res", (self.size[0] / 2, 240), self, 0, min_value=0, max_value=1.5,
                                                 tooltip="I manually control the nasality of the sound"))

        self.name = "VCF"

    def update(self):
        """
        update updates the parameters based on potentiometers
        """
        if self.pins[1].connected_to == None:
            self.module.freq = self.potentiometers[0].val

        self.module.res = self.potentiometers[1].val

    def draw(self, surface):
        """
        draw draws the module

        args
            surface (Surface) - the main drawing surface
        """
        super().draw(surface)

        text_surface = self.font.render('VCF', False, TEXT_COLOR)
        surface.blit(text_surface, (self.pos[0] + 80, self.pos[1] + 15))