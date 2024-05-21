from normal_myhdl import *

@block
def testbench():
    clk = Signal(True)
    reset = Signal(0)
    state_out = Signal(modbv(0)[1:])

    uut = FSM(
        clk=clk,
        reset=reset,
        state_out=state_out
    )

    @instance
    def driver():
        clk.next = 0
        # yield delay(0)
        while 1:
            yield delay(10)
            clk.next = not clk

    @instance
    def test():
        reset.next = 1
        yield delay(40)
        reset.next = 0
        yield delay(1000)

        raise StopSimulation

    @always(reset, state_out)
    def monitor():
        print(f"Time = {now()}, reset = {reset}, state_out = {state_out}")

    return instances()

tb = testbench()
tb.run_sim()
