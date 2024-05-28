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
# 除法模块
# 试商法实现32位整数除法
# 每次除法运算至少需要33个时钟周期才能完成
from myhdl import *

@block
def div (
    clk,
    rst,
    # from ex
    dividend_i,
    # 被除数
    divisor_i,
    # 除数
    start_i,
    # 开始信号，运算期间这个信号需要一直保持有效
    op_i,
    # 具体是哪一条指令
    reg_waddr_i,
    # 运算结束后需要写的寄存器
    # to ex
    result_o,
    # 除法结果，高32位是余数，低32位是商
    ready_o,
    # 运算结束信号
    busy_o,
    # 正在运算信号
    reg_waddr_o
):
    # 状态定义
    # 状态定义
    STATE_IDLE = modbv(0b0001)[4:]
    STATE_START = modbv(0b0010)[4:]
    STATE_CALC = modbv(0b0100)[4:]
    STATE_END = modbv(0b1000)[4:]
    dividend_r = Signal(modbv(0)[31 + 1 - 0:])
    divisor_r = Signal(modbv(0)[31 + 1 - 0:])
    op_r = Signal(modbv(0)[2 + 1 - 0:])
    state = Signal(modbv(0)[3 + 1 - 0:])
    count = Signal(modbv(0)[31 + 1 - 0:])
    div_result = Signal(modbv(0)[31 + 1 - 0:])
    div_remain = Signal(modbv(0)[31 + 1 - 0:])
    minuend = Signal(modbv(0)[31 + 1 - 0:])
    invert_result = Signal(modbv(0)[1:])
    op_div = Signal(modbv(0)[1:])
    @always_comb
    def assign_op_div():
        op_div.next = op_r == 0b100
    op_divu = Signal(modbv(0)[1:])
    @always_comb
    def assign_op_divu():
        op_divu.next = op_r == 0b101
    op_rem = Signal(modbv(0)[1:])
    @always_comb
    def assign_op_rem():
        op_rem.next = op_r == 0b110
    op_remu = Signal(modbv(0)[1:])
    @always_comb
    def assign_op_remu():
        op_remu.next = op_r == 0b111
    dividend_invert = Signal(modbv(0)[31 + 1 - 0:])
    @always_comb
    def assign_dividend_invert():
        dividend_invert.next = -dividend_r
    divisor_invert = Signal(modbv(0)[31 + 1 - 0:])
    @always_comb
    def assign_divisor_invert():
        divisor_invert.next = -divisor_r
    minuend_ge_divisor = Signal(modbv(0)[1:])
    @always_comb
    def assign_minuend_ge_divisor():
        minuend_ge_divisor.next = minuend >= divisor_r
    minuend_sub_res = Signal(modbv(0)[31 + 1 - 0:])
    @always_comb
    def assign_minuend_sub_res():
        minuend_sub_res.next = minuend - divisor_r
    div_result_tmp = Signal(modbv(0)[31 + 1 - 0:])
    @always_comb
    def assign_div_result_tmp():
        div_result_tmp.next = concat(div_result[30 + 1:0], modbv(0b1)[1:]) if minuend_ge_divisor else concat(div_result[30 + 1:0], modbv(0b0)[1:])
    minuend_tmp = Signal(modbv(0)[31 + 1 - 0:])
    @always_comb
    def assign_minuend_tmp():
        minuend_tmp.next = minuend_sub_res[30 + 1:0] if minuend_ge_divisor else minuend[30 + 1:0]

    # 状态机实现
    @always(clk.posedge)
    def seq_0():
        if rst == 0b0: 
            state.next = STATE_IDLE
            ready_o.next = 0b0
            result_o.next = 0x0
            div_result.next = 0x0
            div_remain.next = 0x0
            op_r.next = 0x0
            reg_waddr_o.next = 0x0
            dividend_r.next = 0x0
            divisor_r.next = 0x0
            minuend.next = 0x0
            invert_result.next = 0b0
            busy_o.next = 0b0
            count.next = 0x0

        else:
            if state == STATE_IDLE:
                if start_i == 0b1: 
                    op_r.next = op_i
                    dividend_r.next = dividend_i
                    divisor_r.next = divisor_i
                    reg_waddr_o.next = reg_waddr_i
                    state.next = STATE_START
                    busy_o.next = 0b1

                else: 
                    op_r.next = 0x0
                    reg_waddr_o.next = 0x0
                    dividend_r.next = 0x0
                    divisor_r.next = 0x0
                    ready_o.next = 0b0
                    result_o.next = 0x0
                    busy_o.next = 0b0

            elif state == STATE_START:
                if start_i == 0b1:
                    # 除数为0
                    if divisor_r == 0x0: 
                        if op_div | op_divu:
                            result_o.next = 0xffffffff
                        else:
                            result_o.next = dividend_r
                        ready_o.next = 0b1
                        state.next = STATE_IDLE
                        busy_o.next = 0b0

                    else: 
                        busy_o.next = 0b1
                        count.next = 0x40000000
                        state.next = STATE_CALC
                        div_result.next = 0x0
                        div_remain.next = 0x0
                        # DIV和REM这两条指令是有符号数运算指令
                        if op_div | op_rem: 
                            # 被除数求补码
                            if dividend_r[31] == 0b1: 
                                dividend_r.next = dividend_invert
                                minuend.next = dividend_invert[31]

                            else:
                                minuend.next = dividend_r[31]
                            # 除数求补码
                            if divisor_r[31] == 0b1:
                                divisor_r.next = divisor_invert

                        else:
                            minuend.next = dividend_r[31]
                        # 运算结束后是否要对结果取补码
                        if op_div and dividend_r[31] ^ divisor_r[31] == 0b1 or (op_rem and dividend_r[31] == 0b1):
                            invert_result.next = 0b1
                        else:
                            invert_result.next = 0b0

                else: 
                    state.next = STATE_IDLE
                    result_o.next = 0x0
                    ready_o.next = 0b0
                    busy_o.next = 0b0

            elif state == STATE_CALC:
                if start_i == 0b1: 
                    dividend_r.next = concat(dividend_r[30 + 1:0], modbv(0b0)[1:])
                    div_result.next = div_result_tmp
                    count.next = concat(modbv(0b0)[1:], count[31 + 1:1])
                    if count != 0:
                        minuend.next = concat(minuend_tmp[30 + 1:0], dividend_r[30])
                    else: 
                        state.next = STATE_END
                        if minuend_ge_divisor:
                            div_remain.next = minuend_sub_res
                        else:
                            div_remain.next = minuend


                else: 
                    state.next = STATE_IDLE
                    result_o.next = 0x0
                    ready_o.next = 0b0
                    busy_o.next = 0b0

            elif state == STATE_END:
                if start_i == 0b1: 
                    ready_o.next = 0b1
                    state.next = STATE_IDLE
                    busy_o.next = 0b0
                    if op_div | op_divu:
                        if invert_result:
                            result_o.next = -div_result
                        else:
                            result_o.next = div_result
                    else:
                        if invert_result:
                            result_o.next = -div_remain
                        else:
                            result_o.next = div_remain

                else: 
                    state.next = STATE_IDLE
                    result_o.next = 0x0
                    ready_o.next = 0b0
                    busy_o.next = 0b0


    return instances()
