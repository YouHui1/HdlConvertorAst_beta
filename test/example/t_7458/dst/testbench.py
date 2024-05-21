from _7458_myhdl import *

@block
def testbench():
    p1 = Signal(modbv(0)[7:])
    p2 = Signal(modbv(0)[5:])
    p1y = Signal(modbv(0)[1:])
