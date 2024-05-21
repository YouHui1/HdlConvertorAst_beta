from alu_myhdl import *

@block
def testbench():
    PERIOD = 10
    clk = Signal(True)
    rst = Signal(True)
    io_input1 = Signal(modbv(0)[32:])
    io_input2 = Signal(modbv(0)[32:])
    io_function = Signal(modbv(0)[5:])

    io_output = Signal(modbv(0)[32:])

    uut = ALU(
        clk=clk,
        rst=rst,
        io_input1=io_input1,
        io_input2=io_input2,
        io_function=io_function,
        io_output=io_output
    )

    @instance
    def driver():
        clk.next = 0
        yield delay(0)

        while True:
            yield delay(5)
            clk.next = not clk
    @instance
    def init():
        rst.next = 1
        io_input1.next = 0x1242512f
        io_input2.next = 0xfa34512f
        io_function.next = 0
        print(f'Time = {now()}, rst = {rst}, io_input1 = {io_input1}, io_input2 = {io_input2}, io_function = {io_function}, io_output = {io_output}')
        yield delay(10 * 10)

        rst.next = 0
        print(f'Time = {now()}, rst = {rst}, io_input1 = {io_input1}, io_input2 = {io_input2}, io_function = {io_function}, io_output = {io_output}')
        yield delay(10 * 10)

        io_input1.next = 0x12345678
        io_input2.next = 0x9abcdef
        io_function.next = 0
        print(f'Time = {now()}, rst = {rst}, io_input1 = {io_input1}, io_input2 = {io_input2}, io_function = {io_function}, io_output = {io_output}')
        yield delay(10 * 10)

        io_input1.next = 0x12345678
        io_input2.next = 0x4
        io_function.next = 1
        print(f'Time = {now()}, rst = {rst}, io_input1 = {io_input1}, io_input2 = {io_input2}, io_function = {io_function}, io_output = {io_output}')
        yield delay(10 * 10)

        io_input1.next = 0x12345678
        io_input2.next = 0x9abcdef0
        io_function.next = 2
        print(f'Time = {now()}, rst = {rst}, io_input1 = {io_input1}, io_input2 = {io_input2}, io_function = {io_function}, io_output = {io_output}')
        yield delay(10 * 10)

        io_input1.next = 0x12345678
        io_input2.next = 0x4
        io_function.next = 3
        print(f'Time = {now()}, rst = {rst}, io_input1 = {io_input1}, io_input2 = {io_input2}, io_function = {io_function}, io_output = {io_output}')
        yield delay(10 * 10)

        io_input1.next = 0x12345678
        io_input2.next = 0x9abcdef0
        io_function.next = 4
        print(f'Time = {now()}, rst = {rst}, io_input1 = {io_input1}, io_input2 = {io_input2}, io_function = {io_function}, io_output = {io_output}')
        yield delay(10 * 10)

        io_input1.next = 0x12345678
        io_input2.next = 0x9abcdef0
        io_function.next = 5
        print(f'Time = {now()}, rst = {rst}, io_input1 = {io_input1}, io_input2 = {io_input2}, io_function = {io_function}, io_output = {io_output}')
        yield delay(10 * 10)

        io_input1.next = 0x12345678
        io_input2.next = 0x9abcdef0
        io_function.next = 6
        print(f'Time = {now()}, rst = {rst}, io_input1 = {io_input1}, io_input2 = {io_input2}, io_function = {io_function}, io_output = {io_output}')
        yield delay(10 * 10)

        io_input1.next = 0x12345678
        io_input2.next = 0x4
        io_function.next = 7
        print(f'Time = {now()}, rst = {rst}, io_input1 = {io_input1}, io_input2 = {io_input2}, io_function = {io_function}, io_output = {io_output}')
        yield delay(10 * 10)

        io_input1.next = 0x80000000
        io_input2.next = 0x7fffffff
        io_function.next = 8
        print(f'Time = {now()}, rst = {rst}, io_input1 = {io_input1}, io_input2 = {io_input2}, io_function = {io_function}, io_output = {io_output}')
        yield delay(10 * 10)

        io_input1.next = 0x80000000
        io_input2.next = 0x7fffffff
        io_function.next = 9
        print(f'Time = {now()}, rst = {rst}, io_input1 = {io_input1}, io_input2 = {io_input2}, io_function = {io_function}, io_output = {io_output}')
        yield delay(10 * 10)

        raise StopSimulation

    return instances()

tb = testbench()
tb.run_sim()
