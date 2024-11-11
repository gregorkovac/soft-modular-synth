from pyo import *

class ModuleBase:
    def __init__(self):
        self.outputs = [Sine(440, mul = 1)]

