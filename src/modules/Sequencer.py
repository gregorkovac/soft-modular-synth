from modules.ModuleBase import *
import time

class Sequencer(ModuleBase):
    """
    Sequencer plays a sequence of notes
    """
    def __init__(self, pos):
        super().__init__(pos = pos, size=(300, 310))


        self.bpm = 140
        self.seq_len = 8

        self.prev_time = time.time()

        self.freq_seq = [400 for i in range(self.seq_len)]
        self.i = 0
        
        self.freq = CustomConnection()

        # One output
        self.pins.append(Pin("Out", self.freq, "out", (self.size[0] - 25, 30), self))

        # Frequency potentiometers
        for i in range(int(self.seq_len / 2)):
            self.potentiometers.append(Potentiometer("", (50 + 2 * i * self.size[0] / (self.seq_len + 1), 130), self, 400, min_value=100, max_value=1000))
            self.indicators.append(Indicator((50 + 2 * i * self.size[0] / (self.seq_len + 1), 175), self, 0, 1))

        for i in range(int(self.seq_len / 2)):
            self.potentiometers.append(Potentiometer("", (50 + 2 * i * self.size[0] / (self.seq_len + 1), 220), self, 400, min_value=100, max_value=1000))
            self.indicators.append(Indicator((50 + 2 * i * self.size[0] / (self.seq_len + 1), 265), self, 0, 1))

        self.potentiometers.append(Potentiometer("BPM", (40, 35), self, 140, min_value=50, max_value=300))

        self.name = "Sequencer"

    def update(self):
        """
        update updates the parameters based on potentiometers
        """

        for i in range(self.seq_len):
            self.freq_seq[i] = self.potentiometers[i].val

        self.bpm = self.potentiometers[-1].val

        if time.time() - self.prev_time >= 60 / self.bpm:
            self.freq.value = self.freq_seq[self.i]

            self.indicators[self.i].val = 1
            self.indicators[(self.i - 1) % self.seq_len].val = 0

            self.i = (self.i + 1) % self.seq_len

            self.prev_time = time.time()

    def draw(self, surface):
        """
        draw draws the module

        args
            surface (Surface) - the main drawing surface
        """
        super().draw(surface)

        text_surface = self.font.render('Sequencer', False, TEXT_COLOR)
        surface.blit(text_surface, (self.pos[0] + self.size[0] / 2 - 50, self.pos[1] + 15))