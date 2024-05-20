# DUT: Reduction and Shift Operations Module
from myhdl import *

@block
def shift_dut (
    in_vector,
    # 8-bit input vector
    out_lsh,
    # Logical shift left output
    out_rsh,
    # Logical shift right output
    out_ash,
    # Arithmetic shift right output
    out_rotl,
    # Rotate left output
    out_rotr
):

    @always_comb
    def assign_0():
        # Logical shift left by 1 bit
        out_lsh.next = in_vector << 1
    @always_comb
    def assign_1():
        # Logical shift right by 1 bit
        out_rsh.next = in_vector >> 1
    @always_comb
    def assign_2():
        # Arithmetic shift right by 1 bit (same as logical shift for positive numbers)
        out_ash.next = in_vector >> 1 | in_vector[len(in_vector) - 1] << len(in_vector) - 1
    @always_comb
    def assign_3():
        # Rotate left by 1 bit
        out_rotl.next = concat(in_vector[0], in_vector[7 + 1:1])
    @always_comb
    def assign_4():
        # Rotate right by 1 bit
        out_rotr.next = concat(in_vector[6 + 1:0], in_vector[7])
    return instances()
