from myhdl import *

@block
def t_7458 (
    p1a,
    p1b,
    p1c,
    p1d,
    p1e,
    p1f,
    p1y,
    p2a,
    p2b,
    p2c,
    p2d,
    p2y
):

    @always_comb
    def assign_0():
        p1y.next = p1a & p1b & p1c | (p1d & p1e & p1f)
    @always_comb
    def assign_1():
        p2y.next = p2a & p2b | (p2d & p2c)
    return instances()
