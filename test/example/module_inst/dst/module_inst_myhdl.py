# 模块 A：一个简单的反相器
from myhdl import *

@block
def inverter (
    a,
    b
):

    @always_comb
    def assign_0():
        b.next = ~a
    return instances()
# 模块 B：一个简单的二输入与门
@block
def and_gate (
    a,
    b,
    c
):

    @always_comb
    def assign_0():
        c.next = a & b
    return instances()
# 模块 C：一个简单的二输入或门
@block
def or_gate (
    a,
    b,
    c
):
    d = Signal(modbv(0)[1:])

    @always_comb
    def assign_0():
        d.next = a | b
    @always_comb
    def assign_1():
        c.next = d
    return instances()
# DUT: Top-level module that instantiates modules A, B, and C
@block
def top_module (
    clk,
    data_in,
    data_out
):
    # Signals for module instances
    not_data = Signal(modbv(0)[1:])
    and_data = Signal(modbv(0)[1:])
    or_data = Signal(modbv(0)[1:])

    @always_comb
    def assign_0():
        # Connect the outputs
        data_out.next[0] = not_data
    @always_comb
    def assign_1():
        data_out.next[1] = and_data
    @always_comb
    def assign_2():
        data_out.next[2] = or_data
    uut_inverter = inverter(
        a=data_in(0),
        b=not_data
    )
    uut_and_gate = and_gate(
        a=data_in(0),
        b=data_in(1),
        c=and_data
    )
    uut_or_gate = or_gate(
        a=data_in(0),
        b=data_in(1),
        c=or_data
    )
    return instances()
