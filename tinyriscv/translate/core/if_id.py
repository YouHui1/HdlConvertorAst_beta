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
# 将指令向译码模块传递
from myhdl import *

@block
def if_id (
    clk,
    rst,
    inst_i,
    # 指令内容
    inst_addr_i,
    # 指令地址
    hold_flag_i,
    # 流水线暂停标志
    int_flag_i,
    # 外设中断输入信号
    int_flag_o,
    inst_o,
    # 指令内容
    inst_addr_o
):
    hold_en = Signal(modbv(0)[1:])
    @always_comb
    def assign_hold_en():
        hold_en.next = hold_flag_i >= 0b010
    inst = Signal(modbv(0)[31 + 1 - 0:])
    inst_addr = Signal(modbv(0)[31 + 1 - 0:])
    int_flag = Signal(modbv(0)[7 + 1 - 0:])

    @always_comb
    def assign_0():
        inst_o.next = inst
    @always_comb
    def assign_1():
        inst_addr_o.next = inst_addr
    @always_comb
    def assign_2():
        int_flag_o.next = int_flag
    return instances()
