#/*
# Copyright 2019 Blue Liang, liangkangnan@163.com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# *//*
# Copyright 2019 Blue Liang, liangkangnan@163.com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# */ I type inst
# L type inst
# S type inst
# R and M type inst
# R type inst
# M type inst
# J type inst
# J type inst
# CSR inst
# CSR reg addr
# common regs
# 通用寄存器模块
from myhdl import *

u_regs = [Signal(modbv(0)[31 + 1 - 0:]) for _ in range(abs((0) - (32 - 1))+1)]

@block
def regs (
    clk,
    rst,
    # from ex
    we_i,
    # 写寄存器标志
    waddr_i,
    # 写寄存器地址
    wdata_i,
    # 写寄存器数据
    # from jtag
    jtag_we_i,
    # 写寄存器标志
    jtag_addr_i,
    # 读、写寄存器地址
    jtag_data_i,
    # 写寄存器数据
    # from id
    raddr1_i,
    # 读寄存器1地址
    # to id
    rdata1_o,
    # 读寄存器1数据
    # from id
    raddr2_i,
    # 读寄存器2地址
    # to id
    rdata2_o,
    # 读寄存器2数据
    # to jtag
    jtag_data_o
):
    regs = u_regs

    # 写寄存器
    @always(clk.posedge)
    def seq_0():
        if rst == 0b1:
            # 优先ex模块写操作
            if we_i == 0b1 and waddr_i != 0x0:
                regs[waddr_i].next = wdata_i
            elif jtag_we_i == 0b1 and jtag_addr_i != 0x0:
                regs[jtag_addr_i].next = jtag_data_i
    # 读寄存器1
    @always_comb
    def comb_0():
        if raddr1_i == 0x0:
            rdata1_o.next = 0x0
        elif raddr1_i == waddr_i and we_i == 0b1:
            rdata1_o.next = wdata_i
        else:
            rdata1_o.next = regs[raddr1_i]
    # 读寄存器2
    @always_comb
    def comb_1():
        if raddr2_i == 0x0:
            rdata2_o.next = 0x0
        elif raddr2_i == waddr_i and we_i == 0b1:
            rdata2_o.next = wdata_i
        else:
            rdata2_o.next = regs[raddr2_i]
    # jtag读寄存器
    @always_comb
    def comb_2():
        if jtag_addr_i == 0x0:
            jtag_data_o.next = 0x0
        else:
            jtag_data_o.next = regs[jtag_addr_i]
    return instances()
