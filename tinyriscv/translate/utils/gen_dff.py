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
# */ 带默认值和控制信号的流水线触发器
from myhdl import *

@block
def gen_pipe_dff (
    clk,
    rst,
    hold_en,
    def_val,
    din,
    qout,
    DW = 32
):
    qout_r = Signal(modbv(0)[DW - 1 + 1 - 0:])

    @always_comb
    def assign_0():
        qout.next = qout_r
    @always(clk.posedge)
    def seq_0():
        if not rst or hold_en:
            qout_r.next = def_val
        else:
            qout_r.next = din
    return instances()
# 复位后输出为0的触发器
@block
def gen_rst_0_dff (
    clk,
    rst,
    din,
    qout,
    DW = 32
):
    qout_r = Signal(modbv(0)[DW - 1 + 1 - 0:])

    @always_comb
    def assign_0():
        qout.next = qout_r
    @always(clk.posedge)
    def seq_1():
        if not rst:
            qout_r.next = concat(*[concat(modbv(0b0)[1:]) for _ in range(DW)])
        else:
            qout_r.next = din
    return instances()
# 复位后输出为1的触发器
@block
def gen_rst_1_dff (
    clk,
    rst,
    din,
    qout,
    DW = 32
):
    qout_r = Signal(modbv(0)[DW - 1 + 1 - 0:])

    @always_comb
    def assign_0():
        qout.next = qout_r
    @always(clk.posedge)
    def seq_2():
        if not rst:
            qout_r.next = concat(*[concat(modbv(0b1)[1:]) for _ in range(DW)])
        else:
            qout_r.next = din
    return instances()
# 复位后输出为默认值的触发器
@block
def gen_rst_def_dff (
    clk,
    rst,
    def_val,
    din,
    qout,
    DW = 32
):
    qout_r = Signal(modbv(0)[DW - 1 + 1 - 0:])

    @always_comb
    def assign_0():
        qout.next = qout_r
    @always(clk.posedge)
    def seq_3():
        if not rst:
            qout_r.next = def_val
        else:
            qout_r.next = din
    return instances()
# 带使能端、复位后输出为0的触发器
@block
def gen_en_dff (
    clk,
    rst,
    en,
    din,
    qout,
    DW = 32
):
    qout_r = Signal(modbv(0)[DW - 1 + 1 - 0:])

    @always_comb
    def assign_0():
        qout.next = qout_r
    @always(clk.posedge)
    def seq_4():
        if not rst:
            qout_r.next = concat(*[concat(modbv(0b0)[1:]) for _ in range(DW)])
        elif en == 0b1:
            qout_r.next = din
    return instances()
