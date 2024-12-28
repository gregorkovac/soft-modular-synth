from modules.ModuleBase import *

class VCO(ModuleBase):
    """
    VCO serves as a basic sound generator
    """
    def __init__(self, pos):
        super().__init__(pos = pos, size=(200, 300))

        # Use LFO with high frequencies, because it provides basic shapes
        self.osc = LFO(440, mul=1, add=0, sharp=1)
        
        # One output
        self.pins.append(Pin("Out", self.osc, "out", (self.size[0] - 25, 30), self, tooltip="I output sound"))

        # Modifiers for amplitude and frequency
        self.pins.append(PinModifier("Amp", self.osc, "in", (25, 30), self, "mul", tooltip="I change the volume based on the input signal"))
        self.pins.append(PinModifier("Freq", self.osc, "in", (25, 110), self, "freq", tooltip="I change the pitch based on the input signal"))

        # Potentiometers for frequency and shape
        self.potentiometers.append(Potentiometer("Freq", (self.size[0] / 2, 120), self, 400, min_value=100, max_value=10000, tooltip="I control the pitch"))
        self.potentiometers.append(Potentiometer("Shape", (self.size[0] / 2, 220), self, 0, min_value=0, max_value=3.9, 
                                                 tooltip_value_map=self.tooltip_value_map, tooltip="I control the shape of the sound"))

        self.name = "VCO"

    def tooltip_value_map(self, val):
        if val < 1:
            return "Sine"
        if val < 2:
            return "Saw"
        if val < 3:
            return "Square"
        if val < 4:
            return "Triangle"

    def update(self):
        """
        update updates the parameters based on potentiometers
        """

        osc_type = int(np.floor(self.potentiometers[1].val))

        self.osc.sharp = 1
        if osc_type == 0:
            osc_type = 7
            self.osc.sharp = 0
        elif osc_type == 1:
            osc_type = 0

        self.osc.type = osc_type

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