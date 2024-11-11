from pyo import *
import numpy as np
from MasterSynth import MasterSynth

# s = Server().boot()

# f = Osc(table=TriangleTable(), freq=1)
# a = Sine(mul=f, freq=500).out()
# f.play()
# s.start()

# i = 0
# while True:
#     i += 1

#     print(i)
#     if i % 1000000 == 0:
#         a.mul = 1
#     if i % 100000 == 0:
#         f.freq += 0.5

    
master_synth = MasterSynth()
master_synth.start()