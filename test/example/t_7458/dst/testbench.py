from myhdl import *
from t_7458_myhdl import *

@block
def testbench():
    p1 = Signal(modbv(0)[7:])
    p2 = Signal(modbv(0)[5:])
    p1y = Signal(modbv(0)[1:])
    p2y = Signal(modbv(0)[1:])

    uut = t_7458(
        p1a=p1(0),
        p1b=p1(1),
        p1c=p1(2),
        p1d=p1(3),
        p1e=p1(4),
        p1f=p1(5),
        p1y=p1y,
        p2a=p2(0),
        p2b=p2(1),
        p2c=p2(2),
        p2d=p2(3),
        p2y=p2y
    )

    @instance
    def driver():
        yield delay(0)
        while p1 < 4:
            while p2 < 4:
                yield delay(10)
                print(f"time: {now()}, p1: {p1} p2: {p2} | p1y: {p1y} p2y: {p2y}")
                p2.next += 1
                yield delay(0)
            p1.next += 1
            p2.next = 0
            yield delay(0)

    return instances()

tb = testbench()
tb.run_sim()
