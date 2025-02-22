from modules.ModuleBase import *

class Mix(ModuleBase):
    """
    Mix serves as a mixer with four inputs and two outputs
    """
    def __init__(self, pos):
        super().__init__(pos = pos, size=(200, 340))

        self.module = Mixer(outs=2, chnls=4)

        # Four input pins
        tt = "I take in a signal"
        self.pins.append(Pin("In1", self.module, "in", (25, 80), self, in_channel=0, tooltip=tt))
        self.pins.append(Pin("In2", self.module, "in", (25, 150), self, in_channel=1, tooltip=tt))
        self.pins.append(Pin("In3", self.module, "in", (25, 220), self, in_channel=2, tooltip=tt))
        self.pins.append(Pin("In4", self.module, "in", (25, 290), self, in_channel=3, tooltip=tt))

        # Two output pins
        tt = "I output a mix of the input signals"
        self.pins.append(Pin("Out", self.module[0], "out", (self.size[0] - 25, self.size[1] / 3), self, tooltip=tt))
        self.pins.append(Pin("Out", self.module[1], "out", (self.size[0] - 25, 2 * self.size[1] / 3), self, tooltip=tt))

        # Four potentiometers
        tt = "I control the volume of the input signal to the left of me"
        self.potentiometers.append(Potentiometer("", (80, 80), self, 1, min_value=0, max_value=1, tooltip=tt))
        self.potentiometers.append(Potentiometer("", (80, 150), self, 1, min_value=0, max_value=1, tooltip=tt))
        self.potentiometers.append(Potentiometer("", (80, 220), self, 1, min_value=0, max_value=1, tooltip=tt))
        self.potentiometers.append(Potentiometer("", (80, 290), self, 1, min_value=0, max_value=1, tooltip=tt))

        self.name = "Mixer"

    def update(self):
        """
        update updates parameters based on potentiometers
        """
        for i in range(0, 2):
            self.module.setAmp(0, i, self.potentiometers[0].val)
            self.module.setAmp(1, i, self.potentiometers[1].val)
            self.module.setAmp(2, i, self.potentiometers[2].val)
            self.module.setAmp(3, i, self.potentiometers[3].val)

    def draw(self, surface):
        """
        draw draws the module

        args
            surface (Surface) - the main drawing surface
        """
        super().draw(surface)

        text_surface = self.font.render('MIXER', False, TEXT_COLOR)
        surface.blit(text_surface, (self.pos[0] + 60, self.pos[1] + 15))

        # text_surface = self.font.render('Out', False, TEXT_COLOR)
        # surface.blit(text_surface, (self.pos[0] + self.size[0] - 50, self.pos[1] + self.size[1] / 2 + 15))