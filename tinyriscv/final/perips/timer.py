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
# 32 bits count up timer module
from myhdl import *

@block
def timer (
    clk,
    rst,
    data_i,
    addr_i,
    we_i,
    data_o,
    int_sig_o
):
    REG_CTRL = modbv(0x0)[4:]
    REG_COUNT = modbv(0x4)[4:]
    REG_VALUE = modbv(0x8)[4:]
    # [0]: timer enable
    # [1]: timer int enable
    # [2]: timer int pending, write 1 to clear it
    # addr offset: 0x00
    timer_ctrl = Signal(modbv(0)[31 + 1 - 0:])
    # timer current count, read only
    # addr offset: 0x04
    timer_count = Signal(modbv(0)[31 + 1 - 0:])
    # timer expired value
    # addr offset: 0x08
    timer_value = Signal(modbv(0)[31 + 1 - 0:])

    @always_comb
    def assign_0():
        int_sig_o.next = 0b1 if (timer_ctrl[2] == 0b1 and timer_ctrl[1] == 0b1) else 0b0
    # counter
    @always(clk.posedge)
    def seq_0():
        if rst == 0b0:
            timer_count.next = 0x0
        else:
            if timer_ctrl[0] == 0b1: 
                timer_count.next = timer_count + 0b1
                if timer_count >= timer_value:
                    timer_count.next = 0x0

            else:
                timer_count.next = 0x0
    # write regs
    @always(clk.posedge)
    def seq_1():
        if rst == 0b0: 
            timer_ctrl.next = 0x0
            timer_value.next = 0x0

        else:
            if we_i == 0b1:
                if addr_i[3 + 1:0] == REG_CTRL:
                    timer_ctrl.next = concat(concat(data_i[31 + 1:3], timer_ctrl[2] & not data_i[2]), data_i[1 + 1:0])
                elif addr_i[3 + 1:0] == REG_VALUE:
                    timer_value.next = data_i

            else:
                if timer_ctrl[0] == 0b1 and timer_count >= timer_value: 
                    timer_ctrl.next[0] = 0b0
                    timer_ctrl.next[2] = 0b1

    # read regs
    @always_comb
    def comb_0():
        if rst == 0b0:
            data_o.next = 0x0
        else:
            if addr_i[3 + 1:0] == REG_VALUE:
                data_o.next = timer_value
            elif addr_i[3 + 1:0] == REG_CTRL:
                data_o.next = timer_ctrl
            elif addr_i[3 + 1:0] == REG_COUNT:
                data_o.next = timer_count
            else:
                data_o.next = 0x0
    return instances()
