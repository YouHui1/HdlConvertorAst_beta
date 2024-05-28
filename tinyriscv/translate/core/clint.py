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
# core local interruptor module
from myhdl import *

@block
def clint (
    clk,
    rst,
    # from core
    int_flag_i,
    #
    # from id
    inst_i,
    #
    inst_addr_i,
    #
    # from ex
    jump_flag_i,
    jump_addr_i,
    div_started_i,
    # from ctrl
    hold_flag_i,
    #
    # from csr_reg
    data_i,
    # CSR
    csr_mtvec,
    # mtvec
    csr_mepc,
    # mepc
    csr_mstatus,
    # mstatus
    global_int_en_i,
    #
    # to ctrl
    hold_flag_o,
    #
    # to csr_reg
    we_o,
    #
    waddr_o,
    #
    raddr_o,
    #
    data_o,
    #
    # to ex
    int_addr_o,
    #
    int_assert_o
):
    S_INT_IDLE = modbv(0b0001)[4:]
    S_INT_SYNC_ASSERT = modbv(0b0010)[4:]
    S_INT_ASYNC_ASSERT = modbv(0b0100)[4:]
    S_INT_MRET = modbv(0b1000)[4:]
    S_CSR_IDLE = modbv(0b00001)[5:]
    S_CSR_MSTATUS = modbv(0b00010)[5:]
    S_CSR_MEPC = modbv(0b00100)[5:]
    S_CSR_MSTATUS_MRET = modbv(0b01000)[5:]
    S_CSR_MCAUSE = modbv(0b10000)[5:]
    int_state = Signal(modbv(0)[3 + 1 - 0:])
    csr_state = Signal(modbv(0)[4 + 1 - 0:])
    inst_addr = Signal(modbv(0)[31 + 1 - 0:])
    cause = Signal(modbv(0)[31 + 1 - 0:])

    @always_comb
    def assign_0():
        hold_flag_o.next = 0b1 if (int_state != S_INT_IDLE | csr_state != S_CSR_IDLE) else 0b0
    @always_comb
    def comb_0():
        if rst == 0b0:
            int_state.next = S_INT_IDLE
        else:
            if inst_i == 0x73 or inst_i == 0x00100073:
                if div_started_i == 0b0:
                    int_state.next = S_INT_SYNC_ASSERT
                else:
                    int_state.next = S_INT_IDLE
            elif int_flag_i != 0x0 and global_int_en_i == 0b1:
                int_state.next = S_INT_ASYNC_ASSERT
            elif inst_i == 0x30200073:
                int_state.next = S_INT_MRET
            else:
                int_state.next = S_INT_IDLE
    @always(clk.posedge)
    def seq_0():
        if rst == 0b0: 
            csr_state.next = S_CSR_IDLE
            cause.next = 0x0
            inst_addr.next = 0x0

        else:
            if csr_state == S_CSR_IDLE:
                if int_state == S_INT_SYNC_ASSERT: 
                    csr_state.next = S_CSR_MEPC
                    if jump_flag_i == 0b1:
                        inst_addr.next = jump_addr_i - 0x4
                    else:
                        inst_addr.next = inst_addr_i
                    if inst_i == 0x73:
                        cause.next = 11
                    elif inst_i == 0x00100073:
                        cause.next = 3
                    else:
                        cause.next = 10

                elif int_state == S_INT_ASYNC_ASSERT: 
                    cause.next = 0x80000004
                    csr_state.next = S_CSR_MEPC
                    if jump_flag_i == 0b1:
                        inst_addr.next = jump_addr_i
                    elif div_started_i == 0b1:
                        inst_addr.next = inst_addr_i - 0x4
                    else:
                        inst_addr.next = inst_addr_i

                elif int_state == S_INT_MRET:
                    csr_state.next = S_CSR_MSTATUS_MRET
            elif csr_state == S_CSR_MEPC:
                csr_state.next = S_CSR_MSTATUS
            elif csr_state == S_CSR_MSTATUS:
                csr_state.next = S_CSR_MCAUSE
            elif csr_state == S_CSR_MCAUSE:
                csr_state.next = S_CSR_IDLE
            elif csr_state == S_CSR_MSTATUS_MRET:
                csr_state.next = S_CSR_IDLE
            else:
                csr_state.next = S_CSR_IDLE
    @always(clk.posedge)
    def seq_1():
        if rst == 0b0: 
            we_o.next = 0b0
            waddr_o.next = 0x0
            data_o.next = 0x0

        else:
            if csr_state == S_CSR_MEPC: 
                we_o.next = 0b1
                waddr_o.next = concat(modbv(0x0)[20:], modbv(0x341)[12:])
                data_o.next = inst_addr

            elif csr_state == S_CSR_MCAUSE: 
                we_o.next = 0b1
                waddr_o.next = concat(modbv(0x0)[20:], modbv(0x342)[12:])
                data_o.next = cause

            elif csr_state == S_CSR_MSTATUS: 
                we_o.next = 0b1
                waddr_o.next = concat(modbv(0x0)[20:], modbv(0x300)[12:])
                data_o.next = concat(concat(csr_mstatus[31 + 1:4], modbv(0b0)[1:]), csr_mstatus[2 + 1:0])

            elif csr_state == S_CSR_MSTATUS_MRET: 
                we_o.next = 0b1
                waddr_o.next = concat(modbv(0x0)[20:], modbv(0x300)[12:])
                data_o.next = concat(concat(csr_mstatus[31 + 1:4], csr_mstatus[7]), csr_mstatus[2 + 1:0])

            else: 
                we_o.next = 0b0
                waddr_o.next = 0x0
                data_o.next = 0x0

    @always(clk.posedge)
    def seq_2():
        if rst == 0b0: 
            int_assert_o.next = 0b0
            int_addr_o.next = 0x0

        else:
            if csr_state == S_CSR_MCAUSE: 
                int_assert_o.next = 0b1
                int_addr_o.next = csr_mtvec

            elif csr_state == S_CSR_MSTATUS_MRET: 
                int_assert_o.next = 0b1
                int_addr_o.next = csr_mepc

            else: 
                int_assert_o.next = 0b0
                int_addr_o.next = 0x0

    return instances()
