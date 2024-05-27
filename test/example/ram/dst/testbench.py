from ram_myhdl import *

@block
def testbench():
    clk = Signal(True)
    rst = Signal(False)
    we_i = Signal(0)
    addr_i = Signal(modbv(0)[32:])
    data_i = Signal(modbv(0)[32:])
    data_o = Signal(modbv(0)[32:])

    uut = ram(
        clk=clk,
        rst=rst,
        we_i=we_i,
        addr_i=addr_i,
        data_i=data_i,
        data_o=data_o
    )

    @always(delay(10))
    def driver():
        clk.next = not clk

    @instance
    def test():
        clk.next = 0
        rst.next = 1
        we_i.next = 0
        addr_i.next = 0
        data_i.next = 0

        yield delay(100)

        rst.next = 0
        yield delay(100)
        rst.next = 1

        we_i.next = 1
        addr_i.next = 0
        data_i.next = 0xAAAAAAAA
        yield delay(20)

        we_i.next = 0
        addr_i.next = 0
        yield delay(20)

        if (data_o == 0xAAAAAAAA):
            print("Test passed: Data read matches data written.")
        else:
            print(f"Test failed: Data {data_o} read does not match data written.")

        yield delay(100)

        we_i.next = 1
        addr_i.next = 0x00001000
        data_i.next = 0xACDAA12A
        yield delay(20)

        we_i.next = 0
        addr_i.next = 0x1000
        yield delay(20)

        if (data_o == 0xACDAA12A):
            print("Test passed: Data read matches data written.")
        else:
            print(f"Test failed: Data {data_o} read does not match data written.")

        raise StopSimulation

    return instances()

tb = testbench()
tb.run_sim()
