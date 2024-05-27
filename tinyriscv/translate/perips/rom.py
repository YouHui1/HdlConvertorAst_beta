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
from myhdl import *

u_rom = [Signal(modbv(0)[31 + 1 - 0:]) for _ in range(abs((0) - (4096 - 1))+1)]

@block
def rom (
    clk,
    rst,
    we_i,
    # write enable
    addr_i,
    # addr
    data_i,
    data_o
):
    _rom = u_rom

    @always(clk.posedge)
    def seq_0():
        if we_i == 0b1:
            _rom[addr_i[31 + 1:2]].next = data_i
    @always_comb
    def comb_0():
        if rst == 0b0:
            data_o.next = 0x0
        else:
            data_o.next = _rom[addr_i[31 + 1:2]]
    return instances()
