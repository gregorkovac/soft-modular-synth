from modules.ModuleBase import *

class MasterOut(ModuleBase):
    def __init__(self, pos):
        super().__init__(pos = pos, size=(300, 300))

        self.module = Mixer(outs=1, chnls=2).out()
        self.pins.append(Pin("In", self.module, "in", (25, 30), self))
        self.name = "Master Out"
        self.mags = []

        self.spectrum = Spectrum(self.module[0], size=1024, function=self.set_mags)
        self.spec_pos = (10, 100)
        self.spec_size= (280, 180)

    def set_mags(self, mags):
        self.mags = mags

    def draw(self, surface):

        super().draw(surface)

        text_surface = self.font.render('MASTER OUT', False, TEXT_COLOR)
        surface.blit(text_surface, (self.pos[0] + 80, self.pos[1]))

        pygame.draw.rect(surface, MODULE_PIN_COLOR_INSIDE, 
                         pygame.Rect(self.pos[0] + self.spec_pos[0], self.pos[1] + self.spec_pos[1], self.spec_size[0], self.spec_size[1]))
        
        factor = self.spec_size[0] / len(self.mags[0])

        for m in self.mags[0]:
            x = self.pos[0] + self.spec_pos[0] + int(m[0] * factor)
            y = self.pos[1] + self.spec_pos[1] + self.spec_size[1]
            h = (400 - m[1]) / 2 + 1
            # pygame.draw.rect(surface, "red", pygame.Rect(x, 0, 1, 10 - (m[1] - 400)))
            pygame.draw.rect(surface, CONNECTION_COLOR, pygame.Rect(x, y - h, 1, h))