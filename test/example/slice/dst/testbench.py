from slice_myhdl import *

@block
def testbench():
    data_in = Signal(modbv(0)[8:])
    slice_plus = Signal(modbv(0)[4:])
    slice_minus = Signal(modbv(0)[4:])

    uut = dut(
        data_in=data_in,
        slice_minus=slice_minus,
        slice_plus=slice_plus
    )

    @instance
    def test():
        yield delay(10)

        data_in.next = 0b11010101
        yield delay(10)

        data_in.next = 0b10101010
        yield delay(10)

        data_in.next = 0b11110000
        yield delay(10)

        raise StopSimulation

    @instance
    def msg():
        while True:
            yield delay(10)

            print(f"data_in = {data_in}, slice_plus = {slice_plus}, slice_minus = {slice_minus}")

        raise StopSimulation

    return instances()

tb = testbench()
tb.run_sim()
