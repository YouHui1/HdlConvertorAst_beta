from myhdl import *

@block
def ALU (
    clk,
    rst,
    io_input1,
    io_input2,
    io_function,
    io_output
):

    @always(io_input1, io_input2, io_function)
    def seq_0():
        if io_function == 0:
            io_output.next = io_input1 + io_input2
        elif io_function == 1:
            io_output.next = io_input1 << io_input2[5 - 1 + 1:0]
        elif io_function == 2:
            io_output.next = io_input1 ^ io_input2
        elif io_function == 3:
            io_output.next = io_input1 >> io_input2[5 - 1 + 1:0] | io_input1[len(io_input1) - 1] << len(io_input1) - 1
        elif io_function == 4:
            io_output.next = io_input1 | io_input2
        elif io_function == 5:
            io_output.next = io_input1 & io_input2
        elif io_function == 6:
            io_output.next = io_input1 - io_input2
        elif io_function == 7:
            io_output.next = ((io_input1).signed() >> io_input2[5 - 1 + 1:0] | (io_input1).signed()[len((io_input1).signed()) - 1] << len((io_input1).signed()) - 1).signed()
        elif io_function == 8:
            io_output.next = concat(modbv(0x0)[31:], (io_input1).signed() < (io_input2).signed())
        elif io_function == 9:
            io_output.next = concat(modbv(0x0)[31:], io_input1 < io_input2)
        else:
            io_output.next = 0

    return instances()
