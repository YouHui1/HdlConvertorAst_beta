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
# */ 将输入打DP拍后输出
from utils.gen_dff import *

@block
def gen_ticks_sync (
    rst,
    clk,
    din,
    dout,
    DP = 2,
    DW = 32
):
    sync_dat = [Signal(modbv(0)[DW - 1 + 1 - 0:]) for _ in range(abs((DP - 1) - (0))+1)]
    rst_0_dff_lst = []

    @always_comb
    def assign_0():
        dout.next = sync_dat[DP - 1]

    @instance
    def generate():
        for i in range(DP):
            if i == 0:
                rst_0_dff_lst.append(gen_rst_0_dff(
                    clk=clk,
                    rst=rst,
                    din=din,
                    qout=sync_dat[0],
                    DW=DW
                ))
                pass

            else:
                rst_0_dff_lst.append(gen_rst_0_dff(
                    clk=clk,
                    rst=rst,
                    din=sync_dat[i - 1],
                    qout=sync_dat[i],
                    DW=DW
                ))
                pass

    return instances()
