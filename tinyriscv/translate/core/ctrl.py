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
# 控制模块
# 发出跳转、暂停流水线信号
from myhdl import *

@block
def ctrl (
    rst,
    # from ex
    jump_flag_i,
    jump_addr_i,
    hold_flag_ex_i,
    # from rib
    hold_flag_rib_i,
    # from jtag
    jtag_halt_flag_i,
    # from clint
    hold_flag_clint_i,
    hold_flag_o,
    # to pc_reg
    jump_flag_o,
    jump_addr_o
):

    @always_comb
    def comb_0(): 
        jump_addr_o.next = jump_addr_i
        jump_flag_o.next = jump_flag_i
        hold_flag_o.next = 0b000
        # 按优先级处理不同模块的请求
        if jump_flag_i == 0b1 or hold_flag_ex_i == 0b1 or hold_flag_clint_i == 0b1:
            hold_flag_o.next = 0b011
        elif hold_flag_rib_i == 0b1:
            hold_flag_o.next = 0b001
        elif jtag_halt_flag_i == 0b1:
            hold_flag_o.next = 0b011
        else:
            hold_flag_o.next = 0b000

    return instances()
