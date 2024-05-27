from myhdl import *

@block
def ram (
    clk,
    rst,
    we_i,
    # write enable
    addr_i,
    # addr
    data_i,
    data_o
):
    _ram = [Signal(modbv(0)[31 + 1 - 0:]) for _ in range(abs((0) - (4096 - 1))+1)]

    @always(clk.posedge)
    def seq_0():
        if we_i == 0b1:
            _ram[addr_i[31 + 1:2]].next = data_i
    @always_comb
    def comb_0():
        if rst == 0b0:
            data_o.next = 0
        else:
            data_o.next = _ram[addr_i[31 + 1:2]]
    return instances()
