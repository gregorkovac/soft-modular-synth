from pyo import *
from modules.ModuleBase import ModuleBase

class MasterSynth:
    def __init__(self):
        self.server = Server().boot()
        self.server.start()
        self.master_out = Mixer(outs=1, chnls=1).out()
        self.connection_A = None
        self.modules = []

    def start(self):

        m = ModuleBase()

        self.connect(pin = m.outputs[0], mixer = None)
        self.connect(pin = 0, mixer = self.master_out)

        while True:
            pass

    def stop(self):
        self.server.stop()

    def connect(self, pin, mixer: Mixer = None):
        if self.connection_A == None:
            self.connection_A = (mixer, pin)
            return

        if mixer == None:
            out_pin = pin
            in_pin = self.connection_A[1]
            in_mixer = self.connection_A[0]
        else:
            out_pin = self.connection_A[1]
            in_pin = pin
            in_mixer = mixer

        in_mixer.delInput(in_pin)
        in_mixer.addInput(in_pin, out_pin)

        # TODO: Replace this
        in_mixer.setAmp(0, 0, 1)

        self.connection_A = None
