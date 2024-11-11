from pyo import *

class MasterSynth:
    def __init__(self):
        self.server = Server().boot()
        self.server.start()

    def start(self):
        a = Sine(mul=1, freq=440).out()
        a1 = Sine(mul=1, freq=500).out()

        mixer = Mixer(outs=1, chnls=1)
        mixer.addInput(0, a)
        mixer.addInput(1, a1)
        mixer.setAmp(0, 0, 0.5)
        mixer.setAmp(1, 1, 0.5)

    
        # f = Osc(table=TriangleTable(), freq=1)
        # # f.play()
        # # ses.start()


        # i = 0
        # while True:
        #     i += 1

        #     print(i)
        #     if i % 1000000 == 0:
        #         a.mul = 1
        #     if i % 100000 == 0:
        #         f.freq += 0.5

        while True:
            pass

    def stop(self):
        self.server.stop()
