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
# 将译码结果向执行模块传递
from utils.gen_dff import *

@block
def id_ex (
    clk,
    rst,
    inst_i,
    # 指令内容
    inst_addr_i,
    # 指令地址
    reg_we_i,
    # 写通用寄存器标志
    reg_waddr_i,
    # 写通用寄存器地址
    reg1_rdata_i,
    # 通用寄存器1读数据
    reg2_rdata_i,
    # 通用寄存器2读数据
    csr_we_i,
    # 写CSR寄存器标志
    csr_waddr_i,
    # 写CSR寄存器地址
    csr_rdata_i,
    # CSR寄存器读数据
    op1_i,
    op2_i,
    op1_jump_i,
    op2_jump_i,
    hold_flag_i,
    # 流水线暂停标志
    op1_o,
    op2_o,
    op1_jump_o,
    op2_jump_o,
    inst_o,
    # 指令内容
    inst_addr_o,
    # 指令地址
    reg_we_o,
    # 写通用寄存器标志
    reg_waddr_o,
    # 写通用寄存器地址
    reg1_rdata_o,
    # 通用寄存器1读数据
    reg2_rdata_o,
    # 通用寄存器2读数据
    csr_we_o,
    # 写CSR寄存器标志
    csr_waddr_o,
    # 写CSR寄存器地址
    csr_rdata_o
):
    hold_en = Signal(modbv(0)[1:])
    @always_comb
    def assign_x0():
        hold_en.next = hold_flag_i >= 0b011

    inst = Signal(modbv(0)[31 + 1 - 0:])
    inst_ff = gen_pipe_dff (
        clk,
        rst,
        hold_en,
        0x00000001,
        inst_i,
        inst,
        DW=32
    )
    inst_addr = Signal(modbv(0)[31 + 1 - 0:])
    inst_addr_ff = gen_pipe_dff (
        clk,
        rst,
        hold_en,
        0x00000000,
        inst_addr_i,
        inst_addr,
        DW=32
    )
    reg_we = Signal(modbv(0)[1:])
    reg_we_ff = gen_pipe_dff (
        clk,
        rst,
        hold_en,
        0x0,
        reg_we_i,
        reg_we,
        DW=1
    )
    reg_waddr = Signal(modbv(0)[4 + 1 - 0:])
    reg_waddr_ff = gen_pipe_dff (
        clk,
        rst,
        hold_en,
        0x0,
        reg_waddr_i,
        reg_waddr,
        DW=5
    )
    reg1_rdata = Signal(modbv(0)[31 + 1 - 0:])
    reg1_rdata_ff = gen_pipe_dff (
        clk,
        rst,
        hold_en,
        0x0,
        reg1_rdata_i,
        reg1_rdata,
        DW=32
    )
    reg2_rdata = Signal(modbv(0)[31 + 1 - 0:])
    reg2_rdata_ff = gen_pipe_dff (
        clk,
        rst,
        hold_en,
        0x0,
        reg2_rdata_i,
        reg2_rdata,
        DW=32
    )
    csr_we = Signal(modbv(0)[1:])
    csr_we_ff = gen_pipe_dff (
        clk,
        rst,
        hold_en,
        0x0,
        csr_we_i,
        csr_we,
        DW=1
    )
    csr_waddr = Signal(modbv(0)[31 + 1 - 0:])
    csr_waddr_ff = gen_pipe_dff (
        clk,
        rst,
        hold_en,
        0x0,
        csr_waddr_i,
        csr_waddr,
        DW=32
    )
    csr_rdata = Signal(modbv(0)[31 + 1 - 0:])
    csr_rdata_ff = gen_pipe_dff (
        clk,
        rst,
        hold_en,
        0x0,
        csr_rdata_i,
        csr_rdata,
        DW=32
    )
    op1 = Signal(modbv(0)[31 + 1 - 0:])
    op1_ff = gen_pipe_dff (
        clk,
        rst,
        hold_en,
        0x0,
        op1_i,
        op1,
        DW=32
    )
    op2 = Signal(modbv(0)[31 + 1 - 0:])
    op2_ff = gen_pipe_dff (
        clk,
        rst,
        hold_en,
        0x0,
        op2_i,
        op2,
        DW=32
    )
    op1_jump = Signal(modbv(0)[31 + 1 - 0:])
    op1_jump_ff = gen_pipe_dff (
        clk,
        rst,
        hold_en,
        0x0,
        op1_jump_i,
        op1_jump,
        DW=32
    )
    op2_jump = Signal(modbv(0)[31 + 1 - 0:])
    op2_jump_ff = gen_pipe_dff (
        clk,
        rst,
        hold_en,
        0x0,
        op2_jump_i,
        op2_jump,
        DW=32
    )

    @always_comb
    def assign_0():
        inst_o.next = inst
    @always_comb
    def assign_1():
        inst_addr_o.next = inst_addr
    @always_comb
    def assign_2():
        reg_we_o.next = reg_we
    @always_comb
    def assign_3():
        reg_waddr_o.next = reg_waddr
    @always_comb
    def assign_4():
        reg1_rdata_o.next = reg1_rdata
    @always_comb
    def assign_5():
        reg2_rdata_o.next = reg2_rdata
    @always_comb
    def assign_6():
        csr_we_o.next = csr_we
    @always_comb
    def assign_7():
        csr_waddr_o.next = csr_waddr
    @always_comb
    def assign_8():
        csr_rdata_o.next = csr_rdata
    @always_comb
    def assign_9():
        op1_o.next = op1
    @always_comb
    def assign_10():
        op2_o.next = op2
    @always_comb
    def assign_11():
        op1_jump_o.next = op1_jump
    @always_comb
    def assign_12():
        op2_jump_o.next = op2_jump
    return instances()
