from modules.ModuleBase import *

class LFOModule(ModuleBase):
    """
    LFOModule is a low frequency oscillator that is primarily used for controlling parameters
    """
    def __init__(self, pos):
        super().__init__(pos = pos, size=(200, 260))

        self.osc = LFO(0.1, mul=1, add=0)

        # The module has one output pin
        self.pins.append(Pin("Out", self.osc, "out", (self.size[0] - 25, 30), self,
                             tooltip="I output a signal. Use me to control parameters."))
        
        # The module has two inputs - shape and frequency
        self.potentiometers.append(Potentiometer("Shape", ( self.size[0] / 2, 100), self, 0.1, min_value=0, max_value=4.9, 
                                                 tooltip_value_map=self.tooltip_value_map, tooltip="I control the signal shape"))
        self.potentiometers.append(Potentiometer("Freq", (self.size[0] / 2, 200), self, 1, min_value=0.1, max_value=10,
                                                 tooltip="I control the oscillation speed"))

        self.indicators.append(Indicator((self.size[0]- 25, 100), self, -1, 1))

        self.name = "LFO"

    def tooltip_value_map(self, val):
        if val < 1:
            return "Saw Up"
        if val < 2:
            return "Saw Down"
        if val < 3:
            return "Square"
        if val < 4:
            return "Triangle"
        if val < 5:
            return "Sine"

    def update(self):
        """
        update updates the parameters based on potentiometers
        """

        osc_type = int(np.floor(self.potentiometers[0].val))
        if osc_type == 4:
            osc_type = 7
            self.osc.sharp = 0
        else:
            self.osc.sharp = 1
        self.osc.type = osc_type

        self.osc.freq = self.potentiometers[1].val

        if self.osc.mul >= 100:
            self.indicators[0].min_val = 300
            self.indicators[0].max_val = 500
        else:
            self.indicators[0].min_val = -1
            self.indicators[0].max_val = 1

        self.indicators[0].val = self.osc.get()

    def draw(self, surface):
        """
        draw draws the module

        args
            surface (Surface) - the main drawing surface
        """

        super().draw(surface)

        text_surface = self.font.render('LFO', False, TEXT_COLOR)
        surface.blit(text_surface, (self.pos[0] + self.size[0] / 2 - 25, self.pos[1] + 15))