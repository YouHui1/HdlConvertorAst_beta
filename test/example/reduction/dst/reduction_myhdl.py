# DUT: Reduction Operations Module
from myhdl import *

@block
def reduction_dut (
    in_vector,
    # 8-bit input vector
    out_and,
    # AND reduction output
    out_or,
    # OR reduction output
    out_nand,
    # NAND reduction output
    out_nor,
    # NOR reduction output
    out_xor,
    # XOR reduction output
    out_nxor
):

    @always_comb
    def assign_0():
        # AND reduction: All bits must be 1 for the output to be 1
        out_and.next = in_vector == in_vector.max - 1
    @always_comb
    def assign_1():
        # OR reduction: At least one bit must be 1 for the output to be 1
        out_or.next = in_vector != 0
    @always_comb
    def assign_2():
        # NAND reduction: At least one bit must be 0 for the output to be 1
        out_nand.next = in_vector != in_vector.max - 1
    @always_comb
    def assign_3():
        # NOR reduction: All bits must be 0 for the output to be 1
        out_nor.next = in_vector == 0
    @always_comb
    def assign_4():
        # XOR reduction: the counts of one bit must be odd for the output to be 1
        out_xor.next = bin(in_vector).count('1') % 2 == 1
    @always_comb
    def assign_5():
        # NXOR reduction: the counts of one bit must be even for the output to be 1
        out_nxor.next = bin(in_vector).count('1') % 2 == 0
    return instances()
