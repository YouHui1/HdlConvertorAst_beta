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
# 执行模块
# 纯组合逻辑电路
from myhdl import *

@block
def ex (
    rst,
    # from id
    inst_i,
    # 指令内容
    inst_addr_i,
    # 指令地址
    reg_we_i,
    # 是否写通用寄存器
    reg_waddr_i,
    # 写通用寄存器地址
    reg1_rdata_i,
    # 通用寄存器1输入数据
    reg2_rdata_i,
    # 通用寄存器2输入数据
    csr_we_i,
    # 是否写CSR寄存器
    csr_waddr_i,
    # 写CSR寄存器地址
    csr_rdata_i,
    # CSR寄存器输入数据
    int_assert_i,
    # 中断发生标志
    int_addr_i,
    # 中断跳转地址
    op1_i,
    op2_i,
    op1_jump_i,
    op2_jump_i,
    # from mem
    mem_rdata_i,
    # 内存输入数据
    # from div
    div_ready_i,
    # 除法运算完成标志
    div_result_i,
    # 除法运算结果
    div_busy_i,
    # 除法运算忙标志
    div_reg_waddr_i,
    # 除法运算结束后要写的寄存器地址
    # to mem
    mem_wdata_o,
    # 写内存数据
    mem_raddr_o,
    # 读内存地址
    mem_waddr_o,
    # 写内存地址
    mem_we_o,
    # 是否要写内存
    mem_req_o,
    # 请求访问内存标志
    # to regs
    reg_wdata_o,
    # 写寄存器数据
    reg_we_o,
    # 是否要写通用寄存器
    reg_waddr_o,
    # 写通用寄存器地址
    # to csr reg
    csr_wdata_o,
    # 写CSR寄存器数据
    csr_we_o,
    # 是否要写CSR寄存器
    csr_waddr_o,
    # 写CSR寄存器地址
    # to div
    div_start_o,
    # 开始除法运算标志
    div_dividend_o,
    # 被除数
    div_divisor_o,
    # 除数
    div_op_o,
    # 具体是哪一条除法指令
    div_reg_waddr_o,
    # 除法运算结束后要写的寄存器地址
    # to ctrl
    hold_flag_o,
    # 是否暂停标志
    jump_flag_o,
    # 是否跳转标志
    jump_addr_o
):
    mem_raddr_index = Signal(modbv(0)[1 + 1 - 0:])
    mem_waddr_index = Signal(modbv(0)[1 + 1 - 0:])
    mul_temp = Signal(modbv(0)[63 + 1 - 0:])
    mul_temp_invert = Signal(modbv(0)[63 + 1 - 0:])
    sr_shift = Signal(modbv(0)[31 + 1 - 0:])
    sri_shift = Signal(modbv(0)[31 + 1 - 0:])
    sr_shift_mask = Signal(modbv(0)[31 + 1 - 0:])
    sri_shift_mask = Signal(modbv(0)[31 + 1 - 0:])
    op1_add_op2_res = Signal(modbv(0)[31 + 1 - 0:])
    op1_jump_add_op2_jump_res = Signal(modbv(0)[31 + 1 - 0:])
    reg1_data_invert = Signal(modbv(0)[31 + 1 - 0:])
    reg2_data_invert = Signal(modbv(0)[31 + 1 - 0:])
    op1_ge_op2_signed = Signal(modbv(0)[1:])
    op1_ge_op2_unsigned = Signal(modbv(0)[1:])
    op1_eq_op2 = Signal(modbv(0)[1:])
    mul_op1 = Signal(modbv(0)[31 + 1 - 0:])
    mul_op2 = Signal(modbv(0)[31 + 1 - 0:])
    opcode = Signal(modbv(0)[6 + 1 - 0:])
    funct3 = Signal(modbv(0)[2 + 1 - 0:])
    funct7 = Signal(modbv(0)[6 + 1 - 0:])
    rd = Signal(modbv(0)[4 + 1 - 0:])
    uimm = Signal(modbv(0)[4 + 1 - 0:])
    reg_wdata = Signal(modbv(0)[31 + 1 - 0:])
    reg_we = Signal(modbv(0)[1:])
    reg_waddr = Signal(modbv(0)[4 + 1 - 0:])
    div_wdata = Signal(modbv(0)[31 + 1 - 0:])
    div_we = Signal(modbv(0)[1:])
    div_waddr = Signal(modbv(0)[4 + 1 - 0:])
    div_hold_flag = Signal(modbv(0)[1:])
    div_jump_flag = Signal(modbv(0)[1:])
    div_jump_addr = Signal(modbv(0)[31 + 1 - 0:])
    hold_flag = Signal(modbv(0)[1:])
    jump_flag = Signal(modbv(0)[1:])
    jump_addr = Signal(modbv(0)[31 + 1 - 0:])
    mem_we = Signal(modbv(0)[1:])
    mem_req = Signal(modbv(0)[1:])
    div_start = Signal(modbv(0)[1:])

    @always_comb
    def assign_0():
        opcode.next = inst_i[6 + 1:0]
    @always_comb
    def assign_1():
        funct3.next = inst_i[14 + 1:12]
    @always_comb
    def assign_2():
        funct7.next = inst_i[31 + 1:25]
    @always_comb
    def assign_3():
        rd.next = inst_i[11 + 1:7]
    @always_comb
    def assign_4():
        uimm.next = inst_i[19 + 1:15]
    @always_comb
    def assign_5():
        sr_shift.next = reg1_rdata_i >> reg2_rdata_i[4 + 1:0]
    @always_comb
    def assign_6():
        sri_shift.next = reg1_rdata_i >> inst_i[24 + 1:20]
    @always_comb
    def assign_7():
        sr_shift_mask.next = 0xffffffff >> reg2_rdata_i[4 + 1:0]
    @always_comb
    def assign_8():
        sri_shift_mask.next = 0xffffffff >> inst_i[24 + 1:20]
    @always_comb
    def assign_9():
        op1_add_op2_res.next = op1_i + op2_i
    @always_comb
    def assign_10():
        op1_jump_add_op2_jump_res.next = op1_jump_i + op2_jump_i
    @always_comb
    def assign_11():
        reg1_data_invert.next = ~reg1_rdata_i + 1
    @always_comb
    def assign_12():
        reg2_data_invert.next = ~reg2_rdata_i + 1
    @always_comb
    def assign_13():
        # 有符号数比较
        op1_ge_op2_signed.next = (op1_i).signed() >= (op2_i).signed()
    @always_comb
    def assign_14():
        # 无符号数比较
        op1_ge_op2_unsigned.next = op1_i >= op2_i
    @always_comb
    def assign_15():
        op1_eq_op2.next = op1_i == op2_i
    @always_comb
    def assign_16():
        mul_temp.next = mul_op1 * mul_op2
    @always_comb
    def assign_17():
        mul_temp_invert.next = ~mul_temp + 1
    @always_comb
    def assign_18():
        mem_raddr_index.next = reg1_rdata_i + concat(*[inst_i[31] for _ in range(20)], inst_i[32:20]) & 0b11
    @always_comb
    def assign_19():
        mem_waddr_index.next = reg1_rdata_i + concat(*[inst_i[31] for _ in range(20)], inst_i[31 + 1:25], inst_i[11 + 1:7]) & 0b11
    @always_comb
    def assign_20():
        div_start_o.next = 0b0 if (int_assert_i == 0b1) else div_start
    @always_comb
    def assign_21():
        reg_wdata_o.next = reg_wdata | div_wdata
    @always_comb
    def assign_22():
        # 响应中断时不写通用寄存器
        reg_we_o.next = 0b0 if (int_assert_i == 0b1) else (reg_we or div_we)
    @always_comb
    def assign_23():
        reg_waddr_o.next = reg_waddr | div_waddr
    @always_comb
    def assign_24():
        # 响应中断时不写内存
        mem_we_o.next = 0b0 if (int_assert_i == 0b1) else mem_we
    @always_comb
    def assign_25():
        # 响应中断时不向总线请求访问内存
        mem_req_o.next = 0b0 if (int_assert_i == 0b1) else mem_req
    @always_comb
    def assign_26():
        hold_flag_o.next = hold_flag or div_hold_flag
    @always_comb
    def assign_27():
        jump_flag_o.next = jump_flag or div_jump_flag or (0b1 if (int_assert_i == 0b1) else 0b0)
    @always_comb
    def assign_28():
        jump_addr_o.next = int_addr_i if (int_assert_i == 0b1) else (jump_addr | div_jump_addr)
    @always_comb
    def assign_29():
        # 响应中断时不写CSR寄存器
        csr_we_o.next = 0b0 if (int_assert_i == 0b1) else csr_we_i
    @always_comb
    def assign_30():
        csr_waddr_o.next = csr_waddr_i
    # 处理乘法指令
    @always_comb
    def comb_0():
        if opcode == 0b0110011 and funct7 == 0b0000001:
            if funct3 == 0b000:
                mul_op1.next = reg1_rdata_i
                mul_op2.next = reg2_rdata_i

            elif funct3 == 0b011:
                mul_op1.next = reg1_rdata_i
                mul_op2.next = reg2_rdata_i

            elif funct3 == 0b010:
                mul_op1.next = reg1_data_invert if (reg1_rdata_i[31] == 0b1) else reg1_rdata_i
                mul_op2.next = reg2_rdata_i

            elif funct3 == 0b001:
                mul_op1.next = reg1_data_invert if (reg1_rdata_i[31] == 0b1) else reg1_rdata_i
                mul_op2.next = reg2_data_invert if (reg2_rdata_i[31] == 0b1) else reg2_rdata_i

            else:
                mul_op1.next = reg1_rdata_i
                mul_op2.next = reg2_rdata_i

        else:
            mul_op1.next = reg1_rdata_i
            mul_op2.next = reg2_rdata_i

    # 处理除法指令
    @always_comb
    def comb_1():
        div_dividend_o.next = reg1_rdata_i
        div_divisor_o.next = reg2_rdata_i
        div_op_o.next = funct3
        div_reg_waddr_o.next = reg_waddr_i
        if opcode == 0b0110011 and funct7 == 0b0000001:
            div_we.next = 0b0
            div_wdata.next = 0x0
            div_waddr.next = 0x0
            if funct3 == 0b100:
                div_start.next = 0b1
                div_jump_flag.next = 0b1
                div_hold_flag.next = 0b1
                div_jump_addr.next = op1_jump_add_op2_jump_res

            elif funct3 == 0b101:
                div_start.next = 0b1
                div_jump_flag.next = 0b1
                div_hold_flag.next = 0b1
                div_jump_addr.next = op1_jump_add_op2_jump_res

            elif funct3 == 0b110:
                div_start.next = 0b1
                div_jump_flag.next = 0b1
                div_hold_flag.next = 0b1
                div_jump_addr.next = op1_jump_add_op2_jump_res

            elif funct3 == 0b111:
                div_start.next = 0b1
                div_jump_flag.next = 0b1
                div_hold_flag.next = 0b1
                div_jump_addr.next = op1_jump_add_op2_jump_res

            else:
                div_start.next = 0b0
                div_jump_flag.next = 0b0
                div_hold_flag.next = 0b0
                div_jump_addr.next = 0x0


        else:
            div_jump_flag.next = 0b0
            div_jump_addr.next = 0x0
            if div_busy_i == 0b1:
                div_start.next = 0b1
                div_we.next = 0b0
                div_wdata.next = 0x0
                div_waddr.next = 0x0
                div_hold_flag.next = 0b1

            else:
                div_start.next = 0b0
                div_hold_flag.next = 0b0
                if div_ready_i == 0b1:
                    div_wdata.next = div_result_i
                    div_waddr.next = div_reg_waddr_i
                    div_we.next = 0b1

                else:
                    div_we.next = 0b0
                    div_wdata.next = 0x0
                    div_waddr.next = 0x0




    # 执行
    @always_comb
    def comb_2():
        reg_we.next = reg_we_i
        reg_waddr.next = reg_waddr_i
        mem_req.next = 0b0
        csr_wdata_o.next = 0x0
        if opcode == 0b0010011:
            if funct3 == 0b000:
                jump_flag.next = 0b0
                hold_flag.next = 0b0
                jump_addr.next = 0x0
                mem_wdata_o.next = 0x0
                mem_raddr_o.next = 0x0
                mem_waddr_o.next = 0x0
                mem_we.next = 0b0
                reg_wdata.next = op1_add_op2_res

            elif funct3 == 0b010:
                jump_flag.next = 0b0
                hold_flag.next = 0b0
                jump_addr.next = 0x0
                mem_wdata_o.next = 0x0
                mem_raddr_o.next = 0x0
                mem_waddr_o.next = 0x0
                mem_we.next = 0b0
                reg_wdata.next = concat(*[modbv(~op1_ge_op2_signed)[1:] for _ in range(32)]) & 0x1

            elif funct3 == 0b011:
                jump_flag.next = 0b0
                hold_flag.next = 0b0
                jump_addr.next = 0x0
                mem_wdata_o.next = 0x0
                mem_raddr_o.next = 0x0
                mem_waddr_o.next = 0x0
                mem_we.next = 0b0
                reg_wdata.next = concat(*[modbv(~op1_ge_op2_unsigned)[1:] for _ in range(32)]) & 0x1

            elif funct3 == 0b100:
                jump_flag.next = 0b0
                hold_flag.next = 0b0
                jump_addr.next = 0x0
                mem_wdata_o.next = 0x0
                mem_raddr_o.next = 0x0
                mem_waddr_o.next = 0x0
                mem_we.next = 0b0
                reg_wdata.next = op1_i ^ op2_i

            elif funct3 == 0b110:
                jump_flag.next = 0b0
                hold_flag.next = 0b0
                jump_addr.next = 0x0
                mem_wdata_o.next = 0x0
                mem_raddr_o.next = 0x0
                mem_waddr_o.next = 0x0
                mem_we.next = 0b0
                reg_wdata.next = op1_i | op2_i

            elif funct3 == 0b111:
                jump_flag.next = 0b0
                hold_flag.next = 0b0
                jump_addr.next = 0x0
                mem_wdata_o.next = 0x0
                mem_raddr_o.next = 0x0
                mem_waddr_o.next = 0x0
                mem_we.next = 0b0
                reg_wdata.next = op1_i & op2_i

            elif funct3 == 0b001:
                jump_flag.next = 0b0
                hold_flag.next = 0b0
                jump_addr.next = 0x0
                mem_wdata_o.next = 0x0
                mem_raddr_o.next = 0x0
                mem_waddr_o.next = 0x0
                mem_we.next = 0b0
                reg_wdata.next = reg1_rdata_i << inst_i[24 + 1:20]

            elif funct3 == 0b101:
                jump_flag.next = 0b0
                hold_flag.next = 0b0
                jump_addr.next = 0x0
                mem_wdata_o.next = 0x0
                mem_raddr_o.next = 0x0
                mem_waddr_o.next = 0x0
                mem_we.next = 0b0
                if inst_i[30] == 0b1:
                    reg_wdata.next = sri_shift & sri_shift_mask | (concat(*[modbv(reg1_rdata_i[31])[1:] for _ in range(32)]) & (~sri_shift_mask))
                else:
                    reg_wdata.next = reg1_rdata_i >> inst_i[24 + 1:20]

            else:
                jump_flag.next = 0b0
                hold_flag.next = 0b0
                jump_addr.next = 0x0
                mem_wdata_o.next = 0x0
                mem_raddr_o.next = 0x0
                mem_waddr_o.next = 0x0
                mem_we.next = 0b0
                reg_wdata.next = 0x0

        elif opcode == 0b0110011:
            if funct7 == 0b0000000 or funct7 == 0b0100000:
                if funct3 == 0b000:
                    jump_flag.next = 0b0
                    hold_flag.next = 0b0
                    jump_addr.next = 0x0
                    mem_wdata_o.next = 0x0
                    mem_raddr_o.next = 0x0
                    mem_waddr_o.next = 0x0
                    mem_we.next = 0b0
                    if inst_i[30] == 0b0:
                        reg_wdata.next = op1_add_op2_res
                    else:
                        reg_wdata.next = op1_i - op2_i

                elif funct3 == 0b001:
                    jump_flag.next = 0b0
                    hold_flag.next = 0b0
                    jump_addr.next = 0x0
                    mem_wdata_o.next = 0x0
                    mem_raddr_o.next = 0x0
                    mem_waddr_o.next = 0x0
                    mem_we.next = 0b0
                    reg_wdata.next = op1_i << op2_i[4 + 1:0]

                elif funct3 == 0b010:
                    jump_flag.next = 0b0
                    hold_flag.next = 0b0
                    jump_addr.next = 0x0
                    mem_wdata_o.next = 0x0
                    mem_raddr_o.next = 0x0
                    mem_waddr_o.next = 0x0
                    mem_we.next = 0b0
                    reg_wdata.next = concat(*[modbv(~op1_ge_op2_signed)[1:] for _ in range(32)]) & 0x1

                elif funct3 == 0b011:
                    jump_flag.next = 0b0
                    hold_flag.next = 0b0
                    jump_addr.next = 0x0
                    mem_wdata_o.next = 0x0
                    mem_raddr_o.next = 0x0
                    mem_waddr_o.next = 0x0
                    mem_we.next = 0b0
                    reg_wdata.next = concat(*[modbv(~op1_ge_op2_unsigned)[1:] for _ in range(32)]) & 0x1

                elif funct3 == 0b100:
                    jump_flag.next = 0b0
                    hold_flag.next = 0b0
                    jump_addr.next = 0x0
                    mem_wdata_o.next = 0x0
                    mem_raddr_o.next = 0x0
                    mem_waddr_o.next = 0x0
                    mem_we.next = 0b0
                    reg_wdata.next = op1_i ^ op2_i

                elif funct3 == 0b101:
                    jump_flag.next = 0b0
                    hold_flag.next = 0b0
                    jump_addr.next = 0x0
                    mem_wdata_o.next = 0x0
                    mem_raddr_o.next = 0x0
                    mem_waddr_o.next = 0x0
                    mem_we.next = 0b0
                    if inst_i[30] == 0b1:
                        reg_wdata.next = sr_shift & sr_shift_mask | (concat(*[modbv(reg1_rdata_i[31])[1:] for _ in range(32)]) & (~sr_shift_mask))
                    else:
                        reg_wdata.next = reg1_rdata_i >> reg2_rdata_i[4 + 1:0]

                elif funct3 == 0b110:
                    jump_flag.next = 0b0
                    hold_flag.next = 0b0
                    jump_addr.next = 0x0
                    mem_wdata_o.next = 0x0
                    mem_raddr_o.next = 0x0
                    mem_waddr_o.next = 0x0
                    mem_we.next = 0b0
                    reg_wdata.next = op1_i | op2_i

                elif funct3 == 0b111:
                    jump_flag.next = 0b0
                    hold_flag.next = 0b0
                    jump_addr.next = 0x0
                    mem_wdata_o.next = 0x0
                    mem_raddr_o.next = 0x0
                    mem_waddr_o.next = 0x0
                    mem_we.next = 0b0
                    reg_wdata.next = op1_i & op2_i

                else:
                    jump_flag.next = 0b0
                    hold_flag.next = 0b0
                    jump_addr.next = 0x0
                    mem_wdata_o.next = 0x0
                    mem_raddr_o.next = 0x0
                    mem_waddr_o.next = 0x0
                    mem_we.next = 0b0
                    reg_wdata.next = 0x0

            elif funct7 == 0b0000001:
                if funct3 == 0b000:
                    jump_flag.next = 0b0
                    hold_flag.next = 0b0
                    jump_addr.next = 0x0
                    mem_wdata_o.next = 0x0
                    mem_raddr_o.next = 0x0
                    mem_waddr_o.next = 0x0
                    mem_we.next = 0b0
                    reg_wdata.next = mul_temp[31 + 1:0]

                elif funct3 == 0b011:
                    jump_flag.next = 0b0
                    hold_flag.next = 0b0
                    jump_addr.next = 0x0
                    mem_wdata_o.next = 0x0
                    mem_raddr_o.next = 0x0
                    mem_waddr_o.next = 0x0
                    mem_we.next = 0b0
                    reg_wdata.next = mul_temp[63 + 1:32]

                elif funct3 == 0b001:
                    jump_flag.next = 0b0
                    hold_flag.next = 0b0
                    jump_addr.next = 0x0
                    mem_wdata_o.next = 0x0
                    mem_raddr_o.next = 0x0
                    mem_waddr_o.next = 0x0
                    mem_we.next = 0b0
                    if concat(reg1_rdata_i[31], reg2_rdata_i[31]) == 0b00:
                        reg_wdata.next = mul_temp[63 + 1:32]
                    elif concat(reg1_rdata_i[31], reg2_rdata_i[31]) == 0b11:
                        reg_wdata.next = mul_temp[63 + 1:32]
                    elif concat(reg1_rdata_i[31], reg2_rdata_i[31]) == 0b10:
                        reg_wdata.next = mul_temp_invert[63 + 1:32]
                    else:
                        reg_wdata.next = mul_temp_invert[63 + 1:32]

                elif funct3 == 0b010:
                    jump_flag.next = 0b0
                    hold_flag.next = 0b0
                    jump_addr.next = 0x0
                    mem_wdata_o.next = 0x0
                    mem_raddr_o.next = 0x0
                    mem_waddr_o.next = 0x0
                    mem_we.next = 0b0
                    if reg1_rdata_i[31] == 0b1:
                        reg_wdata.next = mul_temp_invert[63 + 1:32]
                    else:
                        reg_wdata.next = mul_temp[63 + 1:32]

                else:
                    jump_flag.next = 0b0
                    hold_flag.next = 0b0
                    jump_addr.next = 0x0
                    mem_wdata_o.next = 0x0
                    mem_raddr_o.next = 0x0
                    mem_waddr_o.next = 0x0
                    mem_we.next = 0b0
                    reg_wdata.next = 0x0

            else:
                jump_flag.next = 0b0
                hold_flag.next = 0b0
                jump_addr.next = 0x0
                mem_wdata_o.next = 0x0
                mem_raddr_o.next = 0x0
                mem_waddr_o.next = 0x0
                mem_we.next = 0b0
                reg_wdata.next = 0x0

        elif opcode == 0b0000011:
            if funct3 == 0b000:
                jump_flag.next = 0b0
                hold_flag.next = 0b0
                jump_addr.next = 0x0
                mem_wdata_o.next = 0x0
                mem_waddr_o.next = 0x0
                mem_we.next = 0b0
                mem_req.next = 0b1
                mem_raddr_o.next = op1_add_op2_res
                if mem_raddr_index == 0b00:
                    reg_wdata.next = concat(*[mem_rdata_i[7] for _ in range(24)], mem_rdata_i[7 + 1:0])
                elif mem_raddr_index == 0b01:
                    reg_wdata.next = concat(*[mem_rdata_i[15] for _ in range(24)], mem_rdata_i[15 + 1:8])
                elif mem_raddr_index == 0b10:
                    reg_wdata.next = concat(*[mem_rdata_i[23] for _ in range(24)], mem_rdata_i[23 + 1:16])
                else:
                    reg_wdata.next = concat(*[mem_rdata_i[31] for _ in range(24)], mem_rdata_i[31 + 1:24])

            elif funct3 == 0b001:
                jump_flag.next = 0b0
                hold_flag.next = 0b0
                jump_addr.next = 0x0
                mem_wdata_o.next = 0x0
                mem_waddr_o.next = 0x0
                mem_we.next = 0b0
                mem_req.next = 0b1
                mem_raddr_o.next = op1_add_op2_res
                if mem_raddr_index == 0b0:
                    reg_wdata.next = concat(*[mem_rdata_i[15] for _ in range(16)], mem_rdata_i[15 + 1:0])
                else:
                    reg_wdata.next = concat(*[mem_rdata_i[31] for _ in range(16)], mem_rdata_i[31 + 1:16])

            elif funct3 == 0b010:
                jump_flag.next = 0b0
                hold_flag.next = 0b0
                jump_addr.next = 0x0
                mem_wdata_o.next = 0x0
                mem_waddr_o.next = 0x0
                mem_we.next = 0b0
                mem_req.next = 0b1
                mem_raddr_o.next = op1_add_op2_res
                reg_wdata.next = mem_rdata_i

            elif funct3 == 0b100:
                jump_flag.next = 0b0
                hold_flag.next = 0b0
                jump_addr.next = 0x0
                mem_wdata_o.next = 0x0
                mem_waddr_o.next = 0x0
                mem_we.next = 0b0
                mem_req.next = 0b1
                mem_raddr_o.next = op1_add_op2_res
                if mem_raddr_index == 0b00:
                    reg_wdata.next = concat(modbv(0x0)[24:], mem_rdata_i[7 + 1:0])
                elif mem_raddr_index == 0b01:
                    reg_wdata.next = concat(modbv(0x0)[24:], mem_rdata_i[15 + 1:8])
                elif mem_raddr_index == 0b10:
                    reg_wdata.next = concat(modbv(0x0)[24:], mem_rdata_i[23 + 1:16])
                else:
                    reg_wdata.next = concat(modbv(0x0)[24:], mem_rdata_i[31 + 1:24])

            elif funct3 == 0b101:
                jump_flag.next = 0b0
                hold_flag.next = 0b0
                jump_addr.next = 0x0
                mem_wdata_o.next = 0x0
                mem_waddr_o.next = 0x0
                mem_we.next = 0b0
                mem_req.next = 0b1
                mem_raddr_o.next = op1_add_op2_res
                if mem_raddr_index == 0b0:
                    reg_wdata.next = concat(modbv(0x0)[16:], mem_rdata_i[15 + 1:0])
                else:
                    reg_wdata.next = concat(modbv(0x0)[16:], mem_rdata_i[31 + 1:16])

            else:
                jump_flag.next = 0b0
                hold_flag.next = 0b0
                jump_addr.next = 0x0
                mem_wdata_o.next = 0x0
                mem_raddr_o.next = 0x0
                mem_waddr_o.next = 0x0
                mem_we.next = 0b0
                reg_wdata.next = 0x0

        elif opcode == 0b0100011:
            if funct3 == 0b000:
                jump_flag.next = 0b0
                hold_flag.next = 0b0
                jump_addr.next = 0x0
                reg_wdata.next = 0x0
                mem_we.next = 0b1
                mem_req.next = 0b1
                mem_waddr_o.next = op1_add_op2_res
                mem_raddr_o.next = op1_add_op2_res
                if mem_waddr_index == 0b00:
                    mem_wdata_o.next = concat(mem_rdata_i[31 + 1:8], reg2_rdata_i[7 + 1:0])
                elif mem_waddr_index == 0b01:
                    mem_wdata_o.next = concat(concat(mem_rdata_i[31 + 1:16], reg2_rdata_i[7 + 1:0]), mem_rdata_i[7 + 1:0])
                elif mem_waddr_index == 0b10:
                    mem_wdata_o.next = concat(concat(mem_rdata_i[31 + 1:24], reg2_rdata_i[7 + 1:0]), mem_rdata_i[15 + 1:0])
                else:
                    mem_wdata_o.next = concat(reg2_rdata_i[7 + 1:0], mem_rdata_i[23 + 1:0])

            elif funct3 == 0b001:
                jump_flag.next = 0b0
                hold_flag.next = 0b0
                jump_addr.next = 0x0
                reg_wdata.next = 0x0
                mem_we.next = 0b1
                mem_req.next = 0b1
                mem_waddr_o.next = op1_add_op2_res
                mem_raddr_o.next = op1_add_op2_res
                if mem_waddr_index == 0b00:
                    mem_wdata_o.next = concat(mem_rdata_i[31 + 1:16], reg2_rdata_i[15 + 1:0])
                else:
                    mem_wdata_o.next = concat(reg2_rdata_i[15 + 1:0], mem_rdata_i[15 + 1:0])

            elif funct3 == 0b010:
                jump_flag.next = 0b0
                hold_flag.next = 0b0
                jump_addr.next = 0x0
                reg_wdata.next = 0x0
                mem_we.next = 0b1
                mem_req.next = 0b1
                mem_waddr_o.next = op1_add_op2_res
                mem_raddr_o.next = op1_add_op2_res
                mem_wdata_o.next = reg2_rdata_i

            else:
                jump_flag.next = 0b0
                hold_flag.next = 0b0
                jump_addr.next = 0x0
                mem_wdata_o.next = 0x0
                mem_raddr_o.next = 0x0
                mem_waddr_o.next = 0x0
                mem_we.next = 0b0
                reg_wdata.next = 0x0

        elif opcode == 0b1100011:
            if funct3 == 0b000:
                hold_flag.next = 0b0
                mem_wdata_o.next = 0x0
                mem_raddr_o.next = 0x0
                mem_waddr_o.next = 0x0
                mem_we.next = 0b0
                reg_wdata.next = 0x0
                jump_flag.next = op1_eq_op2 & 0b1
                jump_addr.next = concat(*[op1_eq_op2 for _ in range(32)]) & op1_jump_add_op2_jump_res

            elif funct3 == 0b001:
                hold_flag.next = 0b0
                mem_wdata_o.next = 0x0
                mem_raddr_o.next = 0x0
                mem_waddr_o.next = 0x0
                mem_we.next = 0b0
                reg_wdata.next = 0x0
                jump_flag.next = ~op1_eq_op2 & 0b1
                jump_addr.next = concat(*[modbv(~op1_eq_op2)[1:] for _ in range(32)]) & op1_jump_add_op2_jump_res

            elif funct3 == 0b100:
                hold_flag.next = 0b0
                mem_wdata_o.next = 0x0
                mem_raddr_o.next = 0x0
                mem_waddr_o.next = 0x0
                mem_we.next = 0b0
                reg_wdata.next = 0x0
                jump_flag.next = ~op1_ge_op2_signed & 0b1
                jump_addr.next = concat(*[modbv(~op1_ge_op2_signed)[1:] for _ in range(32)]) & op1_jump_add_op2_jump_res

            elif funct3 == 0b101:
                hold_flag.next = 0b0
                mem_wdata_o.next = 0x0
                mem_raddr_o.next = 0x0
                mem_waddr_o.next = 0x0
                mem_we.next = 0b0
                reg_wdata.next = 0x0
                jump_flag.next = op1_ge_op2_signed & 0b1
                jump_addr.next = concat(*[op1_ge_op2_signed for _ in range(32)]) & op1_jump_add_op2_jump_res

            elif funct3 == 0b110:
                hold_flag.next = 0b0
                mem_wdata_o.next = 0x0
                mem_raddr_o.next = 0x0
                mem_waddr_o.next = 0x0
                mem_we.next = 0b0
                reg_wdata.next = 0x0
                jump_flag.next = ~op1_ge_op2_unsigned & 0b1
                jump_addr.next = concat(*[modbv(~op1_ge_op2_unsigned)[1:] for _ in range(32)]) & op1_jump_add_op2_jump_res

            elif funct3 == 0b111:
                hold_flag.next = 0b0
                mem_wdata_o.next = 0x0
                mem_raddr_o.next = 0x0
                mem_waddr_o.next = 0x0
                mem_we.next = 0b0
                reg_wdata.next = 0x0
                jump_flag.next = op1_ge_op2_unsigned & 0b1
                jump_addr.next = concat(*[op1_ge_op2_unsigned for _ in range(32)]) & op1_jump_add_op2_jump_res

            else:
                jump_flag.next = 0b0
                hold_flag.next = 0b0
                jump_addr.next = 0x0
                mem_wdata_o.next = 0x0
                mem_raddr_o.next = 0x0
                mem_waddr_o.next = 0x0
                mem_we.next = 0b0
                reg_wdata.next = 0x0

        elif opcode == 0b1101111:
            hold_flag.next = 0b0
            mem_wdata_o.next = 0x0
            mem_raddr_o.next = 0x0
            mem_waddr_o.next = 0x0
            mem_we.next = 0b0
            jump_flag.next = 0b1
            jump_addr.next = op1_jump_add_op2_jump_res
            reg_wdata.next = op1_add_op2_res

        elif opcode == 0b1100111:
            hold_flag.next = 0b0
            mem_wdata_o.next = 0x0
            mem_raddr_o.next = 0x0
            mem_waddr_o.next = 0x0
            mem_we.next = 0b0
            jump_flag.next = 0b1
            jump_addr.next = op1_jump_add_op2_jump_res
            reg_wdata.next = op1_add_op2_res

        elif opcode == 0b0110111:
            hold_flag.next = 0b0
            mem_wdata_o.next = 0x0
            mem_raddr_o.next = 0x0
            mem_waddr_o.next = 0x0
            mem_we.next = 0b0
            jump_addr.next = 0x0
            jump_flag.next = 0b0
            reg_wdata.next = op1_add_op2_res

        elif opcode == 0b0010111:
            hold_flag.next = 0b0
            mem_wdata_o.next = 0x0
            mem_raddr_o.next = 0x0
            mem_waddr_o.next = 0x0
            mem_we.next = 0b0
            jump_addr.next = 0x0
            jump_flag.next = 0b0
            reg_wdata.next = op1_add_op2_res

        elif opcode == 0b0000001:
            jump_flag.next = 0b0
            hold_flag.next = 0b0
            jump_addr.next = 0x0
            mem_wdata_o.next = 0x0
            mem_raddr_o.next = 0x0
            mem_waddr_o.next = 0x0
            mem_we.next = 0b0
            reg_wdata.next = 0x0

        elif opcode == 0b0001111:
            hold_flag.next = 0b0
            mem_wdata_o.next = 0x0
            mem_raddr_o.next = 0x0
            mem_waddr_o.next = 0x0
            mem_we.next = 0b0
            reg_wdata.next = 0x0
            jump_flag.next = 0b1
            jump_addr.next = op1_jump_add_op2_jump_res

        elif opcode == 0b1110011:
            jump_flag.next = 0b0
            hold_flag.next = 0b0
            jump_addr.next = 0x0
            mem_wdata_o.next = 0x0
            mem_raddr_o.next = 0x0
            mem_waddr_o.next = 0x0
            mem_we.next = 0b0
            if funct3 == 0b001:
                csr_wdata_o.next = reg1_rdata_i
                reg_wdata.next = csr_rdata_i

            elif funct3 == 0b010:
                csr_wdata_o.next = reg1_rdata_i | csr_rdata_i
                reg_wdata.next = csr_rdata_i

            elif funct3 == 0b011:
                csr_wdata_o.next = csr_rdata_i & (~reg1_rdata_i)
                reg_wdata.next = csr_rdata_i

            elif funct3 == 0b101:
                csr_wdata_o.next = concat(modbv(0x0)[27:], uimm)
                reg_wdata.next = csr_rdata_i

            elif funct3 == 0b110:
                csr_wdata_o.next = concat(modbv(0x0)[27:], uimm) | csr_rdata_i
                reg_wdata.next = csr_rdata_i

            elif funct3 == 0b111:
                csr_wdata_o.next = ~(concat(modbv(0x0)[27:], uimm)) & csr_rdata_i
                reg_wdata.next = csr_rdata_i

            else:
                jump_flag.next = 0b0
                hold_flag.next = 0b0
                jump_addr.next = 0x0
                mem_wdata_o.next = 0x0
                mem_raddr_o.next = 0x0
                mem_waddr_o.next = 0x0
                mem_we.next = 0b0
                reg_wdata.next = 0x0


        else:
            jump_flag.next = 0b0
            hold_flag.next = 0b0
            jump_addr.next = 0x0
            mem_wdata_o.next = 0x0
            mem_raddr_o.next = 0x0
            mem_waddr_o.next = 0x0
            mem_we.next = 0b0
            reg_wdata.next = 0x0


    return instances()
