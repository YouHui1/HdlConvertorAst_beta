from myhdl import *

@block
def dut (
    data_in,
    # 8-bit input vector
    slice_plus,
    # Output for addition slice
    slice_minus
):

    # Perform addition slice from bit 4 with a width of 4
    @always(data_in)
    def seq_0():
        slice_plus.next = data_in[4+4-1 + 1:4]
    # Perform subtraction slice from bit 4 with a width of 4
    @always(data_in)
    def seq_1():
        slice_minus.next = data_in[4 + 1:4-4+1]
    return instances()
