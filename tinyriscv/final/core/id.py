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
# 译码模块
# 纯组合逻辑电路
from myhdl import *

@block
def id (
    rst,
    # from if_id
    inst_i,
    # 指令内容
    inst_addr_i,
    # 指令地址
    # from regs
    reg1_rdata_i,
    # 通用寄存器1输入数据
    reg2_rdata_i,
    # 通用寄存器2输入数据
    # from csr reg
    csr_rdata_i,
    # CSR寄存器输入数据
    # from ex
    ex_jump_flag_i,
    # 跳转标志
    # to regs
    reg1_raddr_o,
    # 读通用寄存器1地址
    reg2_raddr_o,
    # 读通用寄存器2地址
    # to csr reg
    csr_raddr_o,
    # 读CSR寄存器地址
    # to ex
    op1_o,
    op2_o,
    op1_jump_o,
    op2_jump_o,
    inst_o,
    # 指令内容
    inst_addr_o,
    # 指令地址
    reg1_rdata_o,
    # 通用寄存器1数据
    reg2_rdata_o,
    # 通用寄存器2数据
    reg_we_o,
    # 写通用寄存器标志
    reg_waddr_o,
    # 写通用寄存器地址
    csr_we_o,
    # 写CSR寄存器标志
    csr_rdata_o,
    # CSR寄存器数据
    csr_waddr_o
):
    opcode = Signal(modbv(inst_i[6 + 1:0])[6 + 1 - 0:])
    @always_comb
    def assign_opcode():
        opcode.next = inst_i[6 + 1:0]
    funct3 = Signal(modbv(inst_i[14 + 1:12])[2 + 1 - 0:])
    @always_comb
    def assign_funct3():
        funct3.next = inst_i[14 + 1:12]
    funct7 = Signal(modbv(inst_i[31 + 1:25])[6 + 1 - 0:])
    @always_comb
    def assign_funct7():
        funct7.next = inst_i[31 + 1:25]
    rd = Signal(modbv(inst_i[11 + 1:7])[4 + 1 - 0:])
    @always_comb
    def assign_rd():
        rd.next = inst_i[11 + 1:7]
    rs1 = Signal(modbv(inst_i[19 + 1:15])[4 + 1 - 0:])
    @always_comb
    def assign_rs1():
        rs1.next = inst_i[19 + 1:15]
    rs2 = Signal(modbv(inst_i[24 + 1:20])[4 + 1 - 0:])
    @always_comb
    def assign_rs2():
        rs2.next = inst_i[24 + 1:20]

    @always_comb
    def comb_0():
        inst_o.next = inst_i
        inst_addr_o.next = inst_addr_i
        reg1_rdata_o.next = reg1_rdata_i
        reg2_rdata_o.next = reg2_rdata_i
        csr_rdata_o.next = csr_rdata_i
        csr_raddr_o.next = 0x0
        csr_waddr_o.next = 0x0
        csr_we_o.next = 0b0
        op1_o.next = 0x0
        op2_o.next = 0x0
        op1_jump_o.next = 0x0
        op2_jump_o.next = 0x0
        if opcode == 0b0010011:
            if funct3 == 0b000:
                reg_we_o.next = 0b1
                reg_waddr_o.next = rd
                reg1_raddr_o.next = rs1
                reg2_raddr_o.next = 0x0
                op1_o.next = reg1_rdata_i
                op2_o.next = concat(concat(concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31])), inst_i[31 + 1:20])

            elif funct3 == 0b010:
                reg_we_o.next = 0b1
                reg_waddr_o.next = rd
                reg1_raddr_o.next = rs1
                reg2_raddr_o.next = 0x0
                op1_o.next = reg1_rdata_i
                op2_o.next = concat(concat(concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31])), inst_i[31 + 1:20])

            elif funct3 == 0b011:
                reg_we_o.next = 0b1
                reg_waddr_o.next = rd
                reg1_raddr_o.next = rs1
                reg2_raddr_o.next = 0x0
                op1_o.next = reg1_rdata_i
                op2_o.next = concat(concat(concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31])), inst_i[31 + 1:20])

            elif funct3 == 0b100:
                reg_we_o.next = 0b1
                reg_waddr_o.next = rd
                reg1_raddr_o.next = rs1
                reg2_raddr_o.next = 0x0
                op1_o.next = reg1_rdata_i
                op2_o.next = concat(concat(concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31])), inst_i[31 + 1:20])

            elif funct3 == 0b110:
                reg_we_o.next = 0b1
                reg_waddr_o.next = rd
                reg1_raddr_o.next = rs1
                reg2_raddr_o.next = 0x0
                op1_o.next = reg1_rdata_i
                op2_o.next = concat(concat(concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31])), inst_i[31 + 1:20])

            elif funct3 == 0b111:
                reg_we_o.next = 0b1
                reg_waddr_o.next = rd
                reg1_raddr_o.next = rs1
                reg2_raddr_o.next = 0x0
                op1_o.next = reg1_rdata_i
                op2_o.next = concat(concat(concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31])), inst_i[31 + 1:20])

            elif funct3 == 0b001:
                reg_we_o.next = 0b1
                reg_waddr_o.next = rd
                reg1_raddr_o.next = rs1
                reg2_raddr_o.next = 0x0
                op1_o.next = reg1_rdata_i
                op2_o.next = concat(concat(concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31])), inst_i[31 + 1:20])

            elif funct3 == 0b101:
                reg_we_o.next = 0b1
                reg_waddr_o.next = rd
                reg1_raddr_o.next = rs1
                reg2_raddr_o.next = 0x0
                op1_o.next = reg1_rdata_i
                op2_o.next = concat(concat(concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31])), inst_i[31 + 1:20])

            else:
                reg_we_o.next = 0b0
                reg_waddr_o.next = 0x0
                reg1_raddr_o.next = 0x0
                reg2_raddr_o.next = 0x0

        elif opcode == 0b0110011:
            if funct7 == 0b0000000 or funct7 == 0b0100000:
                if funct3 == 0b000:
                    reg_we_o.next = 0b1
                    reg_waddr_o.next = rd
                    reg1_raddr_o.next = rs1
                    reg2_raddr_o.next = rs2
                    op1_o.next = reg1_rdata_i
                    op2_o.next = reg2_rdata_i

                elif funct3 == 0b001:
                    reg_we_o.next = 0b1
                    reg_waddr_o.next = rd
                    reg1_raddr_o.next = rs1
                    reg2_raddr_o.next = rs2
                    op1_o.next = reg1_rdata_i
                    op2_o.next = reg2_rdata_i

                elif funct3 == 0b010:
                    reg_we_o.next = 0b1
                    reg_waddr_o.next = rd
                    reg1_raddr_o.next = rs1
                    reg2_raddr_o.next = rs2
                    op1_o.next = reg1_rdata_i
                    op2_o.next = reg2_rdata_i

                elif funct3 == 0b011:
                    reg_we_o.next = 0b1
                    reg_waddr_o.next = rd
                    reg1_raddr_o.next = rs1
                    reg2_raddr_o.next = rs2
                    op1_o.next = reg1_rdata_i
                    op2_o.next = reg2_rdata_i

                elif funct3 == 0b100:
                    reg_we_o.next = 0b1
                    reg_waddr_o.next = rd
                    reg1_raddr_o.next = rs1
                    reg2_raddr_o.next = rs2
                    op1_o.next = reg1_rdata_i
                    op2_o.next = reg2_rdata_i

                elif funct3 == 0b101:
                    reg_we_o.next = 0b1
                    reg_waddr_o.next = rd
                    reg1_raddr_o.next = rs1
                    reg2_raddr_o.next = rs2
                    op1_o.next = reg1_rdata_i
                    op2_o.next = reg2_rdata_i

                elif funct3 == 0b110:
                    reg_we_o.next = 0b1
                    reg_waddr_o.next = rd
                    reg1_raddr_o.next = rs1
                    reg2_raddr_o.next = rs2
                    op1_o.next = reg1_rdata_i
                    op2_o.next = reg2_rdata_i

                elif funct3 == 0b111:
                    reg_we_o.next = 0b1
                    reg_waddr_o.next = rd
                    reg1_raddr_o.next = rs1
                    reg2_raddr_o.next = rs2
                    op1_o.next = reg1_rdata_i
                    op2_o.next = reg2_rdata_i

                else:
                    reg_we_o.next = 0b0
                    reg_waddr_o.next = 0x0
                    reg1_raddr_o.next = 0x0
                    reg2_raddr_o.next = 0x0

            elif funct7 == 0b0000001:
                if funct3 == 0b000:
                    reg_we_o.next = 0b1
                    reg_waddr_o.next = rd
                    reg1_raddr_o.next = rs1
                    reg2_raddr_o.next = rs2
                    op1_o.next = reg1_rdata_i
                    op2_o.next = reg2_rdata_i

                elif funct3 == 0b011:
                    reg_we_o.next = 0b1
                    reg_waddr_o.next = rd
                    reg1_raddr_o.next = rs1
                    reg2_raddr_o.next = rs2
                    op1_o.next = reg1_rdata_i
                    op2_o.next = reg2_rdata_i

                elif funct3 == 0b001:
                    reg_we_o.next = 0b1
                    reg_waddr_o.next = rd
                    reg1_raddr_o.next = rs1
                    reg2_raddr_o.next = rs2
                    op1_o.next = reg1_rdata_i
                    op2_o.next = reg2_rdata_i

                elif funct3 == 0b010:
                    reg_we_o.next = 0b1
                    reg_waddr_o.next = rd
                    reg1_raddr_o.next = rs1
                    reg2_raddr_o.next = rs2
                    op1_o.next = reg1_rdata_i
                    op2_o.next = reg2_rdata_i

                elif funct3 == 0b100:
                    reg_we_o.next = 0b0
                    reg_waddr_o.next = rd
                    reg1_raddr_o.next = rs1
                    reg2_raddr_o.next = rs2
                    op1_o.next = reg1_rdata_i
                    op2_o.next = reg2_rdata_i
                    op1_jump_o.next = inst_addr_i
                    op2_jump_o.next = 0x4

                elif funct3 == 0b101:
                    reg_we_o.next = 0b0
                    reg_waddr_o.next = rd
                    reg1_raddr_o.next = rs1
                    reg2_raddr_o.next = rs2
                    op1_o.next = reg1_rdata_i
                    op2_o.next = reg2_rdata_i
                    op1_jump_o.next = inst_addr_i
                    op2_jump_o.next = 0x4

                elif funct3 == 0b110:
                    reg_we_o.next = 0b0
                    reg_waddr_o.next = rd
                    reg1_raddr_o.next = rs1
                    reg2_raddr_o.next = rs2
                    op1_o.next = reg1_rdata_i
                    op2_o.next = reg2_rdata_i
                    op1_jump_o.next = inst_addr_i
                    op2_jump_o.next = 0x4

                elif funct3 == 0b111:
                    reg_we_o.next = 0b0
                    reg_waddr_o.next = rd
                    reg1_raddr_o.next = rs1
                    reg2_raddr_o.next = rs2
                    op1_o.next = reg1_rdata_i
                    op2_o.next = reg2_rdata_i
                    op1_jump_o.next = inst_addr_i
                    op2_jump_o.next = 0x4

                else:
                    reg_we_o.next = 0b0
                    reg_waddr_o.next = 0x0
                    reg1_raddr_o.next = 0x0
                    reg2_raddr_o.next = 0x0

            else:
                reg_we_o.next = 0b0
                reg_waddr_o.next = 0x0
                reg1_raddr_o.next = 0x0
                reg2_raddr_o.next = 0x0

        elif opcode == 0b0000011:
            if funct3 == 0b000:
                reg1_raddr_o.next = rs1
                reg2_raddr_o.next = 0x0
                reg_we_o.next = 0b1
                reg_waddr_o.next = rd
                op1_o.next = reg1_rdata_i
                op2_o.next = concat(concat(concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31])), inst_i[31 + 1:20])

            elif funct3 == 0b001:
                reg1_raddr_o.next = rs1
                reg2_raddr_o.next = 0x0
                reg_we_o.next = 0b1
                reg_waddr_o.next = rd
                op1_o.next = reg1_rdata_i
                op2_o.next = concat(concat(concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31])), inst_i[31 + 1:20])

            elif funct3 == 0b010:
                reg1_raddr_o.next = rs1
                reg2_raddr_o.next = 0x0
                reg_we_o.next = 0b1
                reg_waddr_o.next = rd
                op1_o.next = reg1_rdata_i
                op2_o.next = concat(concat(concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31])), inst_i[31 + 1:20])

            elif funct3 == 0b100:
                reg1_raddr_o.next = rs1
                reg2_raddr_o.next = 0x0
                reg_we_o.next = 0b1
                reg_waddr_o.next = rd
                op1_o.next = reg1_rdata_i
                op2_o.next = concat(concat(concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31])), inst_i[31 + 1:20])

            elif funct3 == 0b101:
                reg1_raddr_o.next = rs1
                reg2_raddr_o.next = 0x0
                reg_we_o.next = 0b1
                reg_waddr_o.next = rd
                op1_o.next = reg1_rdata_i
                op2_o.next = concat(concat(concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31])), inst_i[31 + 1:20])

            else:
                reg1_raddr_o.next = 0x0
                reg2_raddr_o.next = 0x0
                reg_we_o.next = 0b0
                reg_waddr_o.next = 0x0

        elif opcode == 0b0100011:
            if funct3 == 0b000:
                reg1_raddr_o.next = rs1
                reg2_raddr_o.next = rs2
                reg_we_o.next = 0b0
                reg_waddr_o.next = 0x0
                op1_o.next = reg1_rdata_i
                op2_o.next = concat(concat(concat(concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31])), inst_i[31 + 1:25]), inst_i[11 + 1:7])

            elif funct3 == 0b010:
                reg1_raddr_o.next = rs1
                reg2_raddr_o.next = rs2
                reg_we_o.next = 0b0
                reg_waddr_o.next = 0x0
                op1_o.next = reg1_rdata_i
                op2_o.next = concat(concat(concat(concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31])), inst_i[31 + 1:25]), inst_i[11 + 1:7])

            elif funct3 == 0b001:
                reg1_raddr_o.next = rs1
                reg2_raddr_o.next = rs2
                reg_we_o.next = 0b0
                reg_waddr_o.next = 0x0
                op1_o.next = reg1_rdata_i
                op2_o.next = concat(concat(concat(concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31])), inst_i[31 + 1:25]), inst_i[11 + 1:7])

            else:
                reg1_raddr_o.next = 0x0
                reg2_raddr_o.next = 0x0
                reg_we_o.next = 0b0
                reg_waddr_o.next = 0x0

        elif opcode == 0b1100011:
            if funct3 == 0b000:
                reg1_raddr_o.next = rs1
                reg2_raddr_o.next = rs2
                reg_we_o.next = 0b0
                reg_waddr_o.next = 0x0
                op1_o.next = reg1_rdata_i
                op2_o.next = reg2_rdata_i
                op1_jump_o.next = inst_addr_i
                op2_jump_o.next = concat(concat(concat(concat(concat(concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31])), inst_i[7]), inst_i[30 + 1:25]), inst_i[11 + 1:8]), modbv(0b0)[1:])

            elif funct3 == 0b001:
                reg1_raddr_o.next = rs1
                reg2_raddr_o.next = rs2
                reg_we_o.next = 0b0
                reg_waddr_o.next = 0x0
                op1_o.next = reg1_rdata_i
                op2_o.next = reg2_rdata_i
                op1_jump_o.next = inst_addr_i
                op2_jump_o.next = concat(concat(concat(concat(concat(concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31])), inst_i[7]), inst_i[30 + 1:25]), inst_i[11 + 1:8]), modbv(0b0)[1:])

            elif funct3 == 0b100:
                reg1_raddr_o.next = rs1
                reg2_raddr_o.next = rs2
                reg_we_o.next = 0b0
                reg_waddr_o.next = 0x0
                op1_o.next = reg1_rdata_i
                op2_o.next = reg2_rdata_i
                op1_jump_o.next = inst_addr_i
                op2_jump_o.next = concat(concat(concat(concat(concat(concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31])), inst_i[7]), inst_i[30 + 1:25]), inst_i[11 + 1:8]), modbv(0b0)[1:])

            elif funct3 == 0b101:
                reg1_raddr_o.next = rs1
                reg2_raddr_o.next = rs2
                reg_we_o.next = 0b0
                reg_waddr_o.next = 0x0
                op1_o.next = reg1_rdata_i
                op2_o.next = reg2_rdata_i
                op1_jump_o.next = inst_addr_i
                op2_jump_o.next = concat(concat(concat(concat(concat(concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31])), inst_i[7]), inst_i[30 + 1:25]), inst_i[11 + 1:8]), modbv(0b0)[1:])

            elif funct3 == 0b110:
                reg1_raddr_o.next = rs1
                reg2_raddr_o.next = rs2
                reg_we_o.next = 0b0
                reg_waddr_o.next = 0x0
                op1_o.next = reg1_rdata_i
                op2_o.next = reg2_rdata_i
                op1_jump_o.next = inst_addr_i
                op2_jump_o.next = concat(concat(concat(concat(concat(concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31])), inst_i[7]), inst_i[30 + 1:25]), inst_i[11 + 1:8]), modbv(0b0)[1:])

            elif funct3 == 0b111:
                reg1_raddr_o.next = rs1
                reg2_raddr_o.next = rs2
                reg_we_o.next = 0b0
                reg_waddr_o.next = 0x0
                op1_o.next = reg1_rdata_i
                op2_o.next = reg2_rdata_i
                op1_jump_o.next = inst_addr_i
                op2_jump_o.next = concat(concat(concat(concat(concat(concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31])), inst_i[7]), inst_i[30 + 1:25]), inst_i[11 + 1:8]), modbv(0b0)[1:])

            else:
                reg1_raddr_o.next = 0x0
                reg2_raddr_o.next = 0x0
                reg_we_o.next = 0b0
                reg_waddr_o.next = 0x0

        elif opcode == 0b1101111:
            reg_we_o.next = 0b1
            reg_waddr_o.next = rd
            reg1_raddr_o.next = 0x0
            reg2_raddr_o.next = 0x0
            op1_o.next = inst_addr_i
            op2_o.next = 0x4
            op1_jump_o.next = inst_addr_i
            op2_jump_o.next = concat(concat(concat(concat(concat(concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31])), inst_i[19 + 1:12]), inst_i[20]), inst_i[30 + 1:21]), modbv(0b0)[1:])

        elif opcode == 0b1100111:
            reg_we_o.next = 0b1
            reg1_raddr_o.next = rs1
            reg2_raddr_o.next = 0x0
            reg_waddr_o.next = rd
            op1_o.next = inst_addr_i
            op2_o.next = 0x4
            op1_jump_o.next = reg1_rdata_i
            op2_jump_o.next = concat(concat(concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31]),concat(inst_i[31])), inst_i[31 + 1:20])

        elif opcode == 0b0110111:
            reg_we_o.next = 0b1
            reg_waddr_o.next = rd
            reg1_raddr_o.next = 0x0
            reg2_raddr_o.next = 0x0
            op1_o.next = concat(inst_i[31 + 1:12], modbv(0b0)[12:])
            op2_o.next = 0x0

        elif opcode == 0b0010111:
            reg_we_o.next = 0b1
            reg_waddr_o.next = rd
            reg1_raddr_o.next = 0x0
            reg2_raddr_o.next = 0x0
            op1_o.next = inst_addr_i
            op2_o.next = concat(inst_i[31 + 1:12], modbv(0b0)[12:])

        elif opcode == 0b0000001:
            reg_we_o.next = 0b0
            reg_waddr_o.next = 0x0
            reg1_raddr_o.next = 0x0
            reg2_raddr_o.next = 0x0

        elif opcode == 0b0001111:
            reg_we_o.next = 0b0
            reg_waddr_o.next = 0x0
            reg1_raddr_o.next = 0x0
            reg2_raddr_o.next = 0x0
            op1_jump_o.next = inst_addr_i
            op2_jump_o.next = 0x4

        elif opcode == 0b1110011:
            reg_we_o.next = 0b0
            reg_waddr_o.next = 0x0
            reg1_raddr_o.next = 0x0
            reg2_raddr_o.next = 0x0
            csr_raddr_o.next = concat(modbv(0x0)[20:], inst_i[31 + 1:20])
            csr_waddr_o.next = concat(modbv(0x0)[20:], inst_i[31 + 1:20])
            if funct3 == 0b001:
                reg1_raddr_o.next = rs1
                reg2_raddr_o.next = 0x0
                reg_we_o.next = 0b1
                reg_waddr_o.next = rd
                csr_we_o.next = 0b1

            elif funct3 == 0b010:
                reg1_raddr_o.next = rs1
                reg2_raddr_o.next = 0x0
                reg_we_o.next = 0b1
                reg_waddr_o.next = rd
                csr_we_o.next = 0b1

            elif funct3 == 0b011:
                reg1_raddr_o.next = rs1
                reg2_raddr_o.next = 0x0
                reg_we_o.next = 0b1
                reg_waddr_o.next = rd
                csr_we_o.next = 0b1

            elif funct3 == 0b101:
                reg1_raddr_o.next = 0x0
                reg2_raddr_o.next = 0x0
                reg_we_o.next = 0b1
                reg_waddr_o.next = rd
                csr_we_o.next = 0b1

            elif funct3 == 0b110:
                reg1_raddr_o.next = 0x0
                reg2_raddr_o.next = 0x0
                reg_we_o.next = 0b1
                reg_waddr_o.next = rd
                csr_we_o.next = 0b1

            elif funct3 == 0b111:
                reg1_raddr_o.next = 0x0
                reg2_raddr_o.next = 0x0
                reg_we_o.next = 0b1
                reg_waddr_o.next = rd
                csr_we_o.next = 0b1

            else:
                reg_we_o.next = 0b0
                reg_waddr_o.next = 0x0
                reg1_raddr_o.next = 0x0
                reg2_raddr_o.next = 0x0
                csr_we_o.next = 0b0


        else:
            reg_we_o.next = 0b0
            reg_waddr_o.next = 0x0
            reg1_raddr_o.next = 0x0
            reg2_raddr_o.next = 0x0


    return instances()
