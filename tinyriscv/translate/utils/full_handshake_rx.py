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
# */ 数据接收端模块
# 跨时钟域传输，全(四次)握手协议
# req = 1
# ack_o = 1
# req = 0
# ack_o = 0
from myhdl import *

@block
def full_handshake_rx (
    # RX要接收数据的位宽
    clk,
    # RX端时钟信号
    rst_n,
    # RX端复位信号
    # from tx
    req_i,
    # TX端请求信号
    req_data_i,
    # TX端输入数据
    # to tx
    ack_o,
    # RX端应答TX端信号
    # to rx
    recv_data_o,
    # RX端接收到的数据
    recv_rdy_o,
    DW = 32
):
    STATE_IDLE = modbv(0b01)[2:]
    STATE_DEASSERT = modbv(0b10)[2:]
    state = Signal(modbv(0)[1 + 1 - 0:])
    state_next = Signal(modbv(0)[1 + 1 - 0:])
    req_d = Signal(modbv(0)[1:])
    req = Signal(modbv(0)[1:])
    recv_data = Signal(modbv(0)[DW - 1 + 1 - 0:])
    recv_rdy = Signal(modbv(0)[1:])
    ack = Signal(modbv(0)[1:])

    @always_comb
    def assign_0():
        ack_o.next = ack
    @always_comb
    def assign_1():
        recv_rdy_o.next = recv_rdy
    @always_comb
    def assign_2():
        recv_data_o.next = recv_data
    @always(clk.posedge, rst_n.negedge)
    def seq_0():
        if not rst_n:
            state.next = STATE_IDLE
        else:
            state.next = state_next
    @always_comb
    def comb_0():
        if state == STATE_IDLE:
            if req == 0b1:
                state_next.next = STATE_DEASSERT
            else:
                state_next.next = STATE_IDLE
        elif state == STATE_DEASSERT:
            if req:
                state_next.next = STATE_DEASSERT
            else:
                state_next.next = STATE_IDLE
        else:
            state_next.next = STATE_IDLE
    # 将请求信号打两拍进行同步
    @always(clk.posedge, rst_n.negedge)
    def seq_1():
        if not rst_n: 
            req_d.next = 0b0
            req.next = 0b0

        else: 
            req_d.next = req_i
            req.next = req_d

    @always(clk.posedge, rst_n.negedge)
    def seq_2():
        if not rst_n: 
            ack.next = 0b0
            recv_rdy.next = 0b0
            recv_data.next = concat(*[concat(modbv(0b0)[1:]) for _ in range(DW)])

        else:
            if state == STATE_IDLE:
                if req == 0b1: 
                    ack.next = 0b1
                    recv_rdy.next = 0b1
                    # 这个信号只会持续一个时钟
                    recv_data.next = req_data_i

            elif state == STATE_DEASSERT: 
                recv_rdy.next = 0b0
                recv_data.next = concat(*[concat(modbv(0b0)[1:]) for _ in range(DW)])
                # recv_data <= 0;
                # req撤销后ack也撤销
                if req == 0b0:
                    ack.next = 0b0


    return instances()
