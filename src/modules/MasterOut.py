from modules.ModuleBase import *

class MasterOut(ModuleBase):
    def __init__(self, pos):
        super().__init__(pos = pos, size=(220, 60))

        self.module = Mixer(outs=1, chnls=1).out()
        self.pins.append(Pin(self.module, "in", (25, 30), self))

        self.name = "Master Out"

    def draw(self, surface):
        super().draw(surface)

        text_surface = self.font.render('MASTER OUT', False, TEXT_COLOR)
        surface.blit(text_surface, (self.pos[0] + 60, self.pos[1] + 15))