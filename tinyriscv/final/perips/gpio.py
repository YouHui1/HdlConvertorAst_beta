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
# */ GPIO模块
from myhdl import *

@block
def gpio (
    clk,
    rst,
    we_i,
    addr_i,
    data_i,
    data_o,
    io_pin_i,
    reg_ctrl,
    reg_data
):
    # GPIO控制寄存器
    # GPIO控制寄存器
    GPIO_CTRL = modbv(0x0)[4:]
    # GPIO数据寄存器
    # GPIO数据寄存器
    GPIO_DATA = modbv(0x4)[4:]
    # 每2位控制1个IO的模式，最多支持16个IO
    # 0: 高阻，1：输出，2：输入
    gpio_ctrl = Signal(modbv(0)[31 + 1 - 0:])
    # 输入输出数据
    gpio_data = Signal(modbv(0)[31 + 1 - 0:])

    @always_comb
    def assign_0():
        reg_ctrl.next = gpio_ctrl
    @always_comb
    def assign_1():
        reg_data.next = gpio_data
    # 写寄存器
    @always(clk.posedge)
    def seq_0():
        if rst == 0b0: 
            gpio_data.next = 0x0
            gpio_ctrl.next = 0x0

        else:
            if we_i == 0b1:
                if addr_i[3 + 1:0] == GPIO_CTRL:
                    gpio_ctrl.next = data_i
                elif addr_i[3 + 1:0] == GPIO_DATA:
                    gpio_data.next = data_i

            else: 
                if gpio_ctrl[1 + 1:0] == 0b10:
                    gpio_data.next[0] = io_pin_i[0]
                if gpio_ctrl[3 + 1:2] == 0b10:
                    gpio_data.next[1] = io_pin_i[1]

    # 读寄存器
    @always_comb
    def comb_0():
        if rst == 0b0:
            data_o.next = 0x0
        else:
            if addr_i[3 + 1:0] == GPIO_CTRL:
                data_o.next = gpio_ctrl
            elif addr_i[3 + 1:0] == GPIO_DATA:
                data_o.next = gpio_data
            else:
                data_o.next = 0x0
    return instances()
