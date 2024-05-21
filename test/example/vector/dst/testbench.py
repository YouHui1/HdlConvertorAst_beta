from vector_myhdl import *

@block
def testbench():
    clk = Signal(True)
    a = Signal(modbv(0)[8:])
    b = Signal(modbv(0)[8:])
    out1 = Signal(modbv(0)[16:])
    out2 = Signal(modbv(0)[16:])
    out3 = Signal(modbv(0)[16:])
    out4 = Signal(modbv(0)[16:])
    out5 = Signal(modbv(0)[8:])
    out6 = Signal(modbv(0)[8:])

    dut_inst = dut(
        clk=clk,
        a=a,
        b=b,
        out1=out1,
        out2=out2,
        out3=out3,
        out4=out4,
        out5=out5,
        out6=out6
    )

    @instance
    def test():
        clk.next = 0
        a.next = 0x12
        b.next = 0x34
        yield delay(10)

        a.next = 0x56
        b.next = 0x78
        yield delay(10)

        a.next = 0xab
        b.next = 0xcd
        yield delay(10)

        a.next = 0xef
        b.next = 0x01
        yield delay(10)

        a.next = 0x80
        b.next = 0x80
        yield delay(10)

        a.next = 0xff
        b.next = 0xff
        yield delay(10)

        a.next = 0x00
        b.next = 0x00
        yield delay(10)

        a.next = 0x01
        b.next = 0x02
        yield delay(10)

        a.next = 0x03
        b.next = 0x04
        yield delay(10)

        a.next = 0x05
        b.next = 0x06
        yield delay(10)

        a.next = 0x07
        b.next = 0x08
        yield delay(10)

        a.next = 0x09
        b.next = 0x0a
        yield delay(10)

        a.next = 0x0b
        b.next = 0x0c
        yield delay(10)

        a.next = 0x0d
        b.next = 0x0e
        yield delay(10)

        a.next = 0x0f
        b.next = 0x10
        yield delay(20)

        raise StopSimulation

    @always(delay(5))
    def driver():
        clk.next = not clk

    @always(clk.posedge)
    def msg():
        print(f'a = {a}, b = {b}, out1 = {out1}, out2 = {out2}, out3 = {out3}, out4 = {out4}, out5 = {out5}, out6 = {out6}')

    return instances()

tb = testbench()
tb.run_sim()
