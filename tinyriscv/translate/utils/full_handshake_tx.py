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
# */ 数据发送端模块
# 跨时钟域传输，全(四次)握手协议
# req_o = 1
# ack = 1
# req_o = 0
# ack = 0
from myhdl import *

@block
def full_handshake_tx (
    # TX要发送数据的位宽
    clk,
    # TX端时钟信号
    rst_n,
    # TX端复位信号
    # from rx
    ack_i,
    # RX端应答信号
    # from tx
    req_i,
    # TX端请求信号，只需持续一个时钟
    req_data_i,
    # TX端要发送的数据，只需持续一个时钟
    # to tx
    idle_o,
    # TX端是否空闲信号，空闲才能发数据
    # to rx
    req_o,
    # TX端请求信号
    req_data_o,
    DW = 32
):
    STATE_IDLE = modbv(0b001)[3:]
    STATE_ASSERT = modbv(0b010)[3:]
    STATE_DEASSERT = modbv(0b100)[3:]
    state = Signal(modbv(0)[2 + 1 - 0:])
    state_next = Signal(modbv(0)[2 + 1 - 0:])
    ack_d = Signal(modbv(0)[1:])
    ack = Signal(modbv(0)[1:])
    req = Signal(modbv(0)[1:])
    req_data = Signal(modbv(0)[DW - 1 + 1 - 0:])
    idle = Signal(modbv(0)[1:])

    @always_comb
    def assign_0():
        idle_o.next = idle
    @always_comb
    def assign_1():
        req_o.next = req
    @always_comb
    def assign_2():
        req_data_o.next = req_data
    @always(clk.posedge, rst_n.negedge)
    def seq_0():
        if not rst_n:
            state.next = STATE_IDLE
        else:
            state.next = state_next
    @always_comb
    def comb_0():
        if state == STATE_IDLE:
            if req_i == 0b1:
                state_next.next = STATE_ASSERT
            else:
                state_next.next = STATE_IDLE
        elif state == STATE_ASSERT:
            if not ack:
                state_next.next = STATE_ASSERT
            else:
                state_next.next = STATE_DEASSERT
        elif state == STATE_DEASSERT:
            if not ack:
                state_next.next = STATE_IDLE
            else:
                state_next.next = STATE_DEASSERT
        else:
            state_next.next = STATE_IDLE
    # 将应答信号打两拍进行同步
    @always(clk.posedge, rst_n.negedge)
    def seq_1():
        if not rst_n: 
            ack_d.next = 0b0
            ack.next = 0b0

        else: 
            ack_d.next = ack_i
            ack.next = ack_d

    @always(clk.posedge, rst_n.negedge)
    def seq_2():
        if not rst_n: 
            idle.next = 0b1
            req.next = 0b0
            req_data.next = concat(*[concat(modbv(0b0)[1:]) for _ in range(DW)])

        else:
            if state == STATE_IDLE:
                if req_i == 0b1: 
                    idle.next = 0b0
                    req.next = req_i
                    req_data.next = req_data_i

                else: 
                    idle.next = 0b1
                    req.next = 0b0

            elif state == STATE_ASSERT:
                if ack == 0b1: 
                    req.next = 0b0
                    req_data.next = concat(*[concat(modbv(0b0)[1:]) for _ in range(DW)])

            elif state == STATE_DEASSERT:
                if not ack:
                    idle.next = 0b1

    return instances()
