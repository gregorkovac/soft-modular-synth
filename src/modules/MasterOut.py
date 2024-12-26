from modules.ModuleBase import *

class MasterOut(ModuleBase):
    """
    The MasterOut module serves as a master output and contains a frequency spectrum visualizer
    """

    def __init__(self, pos):
        super().__init__(pos = pos, size=(300, 300))

        self.module = Mixer(outs=1, chnls=2).out()

        # The master output has one input pin
        self.pins.append(Pin("In", self.module, "in", (25, 30), self))

        self.name = "Master Out"
        self.mags = []

        # Initialize Pyo's Spectrum
        self.spectrum = Spectrum(self.module[0], size=1024, function=self.set_mags)

        # Spectrum position
        self.spec_pos = (10, 100)

        # Spectrum size
        self.spec_size = (280, 180)

    def set_mags(self, mags):
        """
        set_mags fetches magnitudes from Spectrum

        args
            mags (list) - list of magnitudes
        """

        self.mags = mags

    def draw(self, surface):
        """
        draw draws the module

        args
            surface (Surface) - the main drawing surface
        """
        
        super().draw(surface)

        text_surface = self.font.render('MASTER OUT', False, TEXT_COLOR)
        surface.blit(text_surface, (self.pos[0] + 80, self.pos[1]))

        # Draw the frequency spectrum
        pygame.draw.rect(surface, MODULE_PIN_COLOR_INSIDE, 
                         pygame.Rect(self.pos[0] + self.spec_pos[0], self.pos[1] + self.spec_pos[1], self.spec_size[0], self.spec_size[1]))
        factor = self.spec_size[0] / len(self.mags[0])
        for m in self.mags[0]:
            x = self.pos[0] + self.spec_pos[0] + int(m[0] * factor)
            y = self.pos[1] + self.spec_pos[1] + self.spec_size[1]
            h = (400 - m[1]) / 2 + 1
            pygame.draw.rect(surface, CONNECTION_COLOR, pygame.Rect(x, y - h, 1, h))