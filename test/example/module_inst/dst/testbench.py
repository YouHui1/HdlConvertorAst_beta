from module_inst_myhdl import *

@block
def testbench():
    clk = Signal(True)
    data_in = Signal(modbv(0)[2:])
    data_out = Signal(modbv(0)[3:])

    uut = top_module(
        clk=clk,
        data_in=data_in,
        data_out=data_out
    )

    @instance
    def driver():
        clk.next = 0
        yield delay(0)
        while True:
            yield delay(5)
            clk.next = not clk

    @instance
    def test():
        print(f"Time = {now()}, data_in = {data_in}, data_out = {data_out}")
        data_in.next = 0
        yield delay(20)
        print(f"Time = {now()}, data_in = {data_in}, data_out = {data_out}")
        data_in.next = 1
        yield delay(20)
        print(f"Time = {now()}, data_in = {data_in}, data_out = {data_out}")
        data_in.next = 2
        yield delay(20)
        print(f"Time = {now()}, data_in = {data_in}, data_out = {data_out}")
        data_in.next = 3
        yield delay(20)
        print(f"Time = {now()}, data_in = {data_in}, data_out = {data_out}")
        yield delay(20)

        raise StopSimulation


    return instances()

tb = testbench()
tb.run_sim()
