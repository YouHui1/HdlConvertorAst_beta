#/*                                                                      
# Copyright 2020 Blue Liang, liangkangnan@163.com
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
# CSR寄存器模块
from myhdl import *

@block
def csr_reg (
    clk,
    rst,
    # form ex
    we_i,
    # ex模块写寄存器标志
    raddr_i,
    # ex模块读寄存器地址
    waddr_i,
    # ex模块写寄存器地址
    data_i,
    # ex模块写寄存器数据
    # from clint
    clint_we_i,
    # clint模块写寄存器标志
    clint_raddr_i,
    # clint模块读寄存器地址
    clint_waddr_i,
    # clint模块写寄存器地址
    clint_data_i,
    # clint模块写寄存器数据
    global_int_en_o,
    # 全局中断使能标志
    # to clint
    clint_data_o,
    # clint模块读寄存器数据
    clint_csr_mtvec,
    # mtvec
    clint_csr_mepc,
    # mepc
    clint_csr_mstatus,
    # mstatus
    # to ex
    data_o
):
    cycle = Signal(modbv(0)[63 + 1 - 0:])
    mtvec = Signal(modbv(0)[31 + 1 - 0:])
    mcause = Signal(modbv(0)[31 + 1 - 0:])
    mepc = Signal(modbv(0)[31 + 1 - 0:])
    mie = Signal(modbv(0)[31 + 1 - 0:])
    mstatus = Signal(modbv(0)[31 + 1 - 0:])
    mscratch = Signal(modbv(0)[31 + 1 - 0:])

    @always_comb
    def assign_0():
        global_int_en_o.next = 0b1 if (mstatus[3] == 0b1) else 0b0
    @always_comb
    def assign_1():
        clint_csr_mtvec.next = mtvec
    @always_comb
    def assign_2():
        clint_csr_mepc.next = mepc
    @always_comb
    def assign_3():
        clint_csr_mstatus.next = mstatus
    # cycle counter
    # 复位撤销后就一直计数
    @always(clk.posedge)
    def seq_0():
        if rst == 0b0:
            cycle.next = concat(modbv(0x0)[32:], modbv(0x0)[32:])
        else:
            cycle.next = cycle + 0b1
    # write reg
    # 写寄存器操作
    @always(clk.posedge)
    def seq_1():
        if rst == 0b0: 
            mtvec.next = 0x0
            mcause.next = 0x0
            mepc.next = 0x0
            mie.next = 0x0
            mstatus.next = 0x0
            mscratch.next = 0x0

        else:
            # 优先响应ex模块的写操作
            if we_i == 0b1:
                if waddr_i[11 + 1:0] == 0x305:
                    mtvec.next = data_i
                elif waddr_i[11 + 1:0] == 0x342:
                    mcause.next = data_i
                elif waddr_i[11 + 1:0] == 0x341:
                    mepc.next = data_i
                elif waddr_i[11 + 1:0] == 0x304:
                    mie.next = data_i
                elif waddr_i[11 + 1:0] == 0x300:
                    mstatus.next = data_i
                elif waddr_i[11 + 1:0] == 0x340:
                    mscratch.next = data_i
                else: 
                    pass

            elif clint_we_i == 0b1:
                if clint_waddr_i[11 + 1:0] == 0x305:
                    mtvec.next = clint_data_i
                elif clint_waddr_i[11 + 1:0] == 0x342:
                    mcause.next = clint_data_i
                elif clint_waddr_i[11 + 1:0] == 0x341:
                    mepc.next = clint_data_i
                elif clint_waddr_i[11 + 1:0] == 0x304:
                    mie.next = clint_data_i
                elif clint_waddr_i[11 + 1:0] == 0x300:
                    mstatus.next = clint_data_i
                elif clint_waddr_i[11 + 1:0] == 0x340:
                    mscratch.next = clint_data_i
                else: 
                    pass

    # read reg
    # ex模块读CSR寄存器
    @always_comb
    def comb_0():
        if waddr_i[11 + 1:0] == raddr_i[11 + 1:0] and we_i == 0b1:
            data_o.next = data_i
        else:
            if raddr_i[11 + 1:0] == 0xc00:
                data_o.next = cycle[31 + 1:0]
            elif raddr_i[11 + 1:0] == 0xc80:
                data_o.next = cycle[63 + 1:32]
            elif raddr_i[11 + 1:0] == 0x305:
                data_o.next = mtvec
            elif raddr_i[11 + 1:0] == 0x342:
                data_o.next = mcause
            elif raddr_i[11 + 1:0] == 0x341:
                data_o.next = mepc
            elif raddr_i[11 + 1:0] == 0x304:
                data_o.next = mie
            elif raddr_i[11 + 1:0] == 0x300:
                data_o.next = mstatus
            elif raddr_i[11 + 1:0] == 0x340:
                data_o.next = mscratch
            else:
                data_o.next = 0x0
    # read reg
    # clint模块读CSR寄存器
    @always_comb
    def comb_1():
        if clint_waddr_i[11 + 1:0] == clint_raddr_i[11 + 1:0] and clint_we_i == 0b1:
            clint_data_o.next = clint_data_i
        else:
            if clint_raddr_i[11 + 1:0] == 0xc00:
                clint_data_o.next = cycle[31 + 1:0]
            elif clint_raddr_i[11 + 1:0] == 0xc80:
                clint_data_o.next = cycle[63 + 1:32]
            elif clint_raddr_i[11 + 1:0] == 0x305:
                clint_data_o.next = mtvec
            elif clint_raddr_i[11 + 1:0] == 0x342:
                clint_data_o.next = mcause
            elif clint_raddr_i[11 + 1:0] == 0x341:
                clint_data_o.next = mepc
            elif clint_raddr_i[11 + 1:0] == 0x304:
                clint_data_o.next = mie
            elif clint_raddr_i[11 + 1:0] == 0x300:
                clint_data_o.next = mstatus
            elif clint_raddr_i[11 + 1:0] == 0x340:
                clint_data_o.next = mscratch
            else:
                clint_data_o.next = 0x0
    return instances()
