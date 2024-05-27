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
# PC寄存器模块
from myhdl import *

@block
def pc_reg (
    clk,
    rst,
    jump_flag_i,
    # 跳转标志
    jump_addr_i,
    # 跳转地址
    hold_flag_i,
    # 流水线暂停标志
    jtag_reset_flag_i,
    # 复位标志
    pc_o
):

    @always(clk.posedge)
    def seq_0():
        # 复位
        if rst == 0b0 or jtag_reset_flag_i == 0b1:
            pc_o.next = 0x0
        elif jump_flag_i == 0b1:
            pc_o.next = jump_addr_i
        elif hold_flag_i >= 0b001:
            pc_o.next = pc_o
        else:
            pc_o.next = pc_o + 0x4
    return instances()
