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
# */ 串口模块(默认: 115200, 8 N 1)
from myhdl import *

@block
def uart (
    clk,
    rst,
    we_i,
    addr_i,
    data_i,
    data_o,
    tx_pin,
    rx_pin
):
    # 50MHz时钟，波特率115200bps对应的分频系数
    # 50MHz时钟，波特率115200bps对应的分频系数
    BAUD_115200 = modbv(0x1b8)[32:]
    S_IDLE = modbv(0b0001)[4:]
    S_START = modbv(0b0010)[4:]
    S_SEND_BYTE = modbv(0b0100)[4:]
    S_STOP = modbv(0b1000)[4:]
    tx_data_valid = Signal(modbv(0)[1:])
    tx_data_ready = Signal(modbv(0)[1:])
    state = Signal(modbv(0)[3 + 1 - 0:])
    cycle_cnt = Signal(modbv(0)[15 + 1 - 0:])
    bit_cnt = Signal(modbv(0)[3 + 1 - 0:])
    tx_data = Signal(modbv(0)[7 + 1 - 0:])
    tx_reg = Signal(modbv(0)[1:])
    rx_q0 = Signal(modbv(0)[1:])
    rx_q1 = Signal(modbv(0)[1:])
    rx_negedge = Signal(modbv(0)[1:])
    rx_start = Signal(modbv(0)[1:])
    # RX使能
    rx_clk_edge_cnt = Signal(modbv(0)[3 + 1 - 0:])
    # clk时钟沿的个数
    rx_clk_edge_level = Signal(modbv(0)[1:])
    # clk沿电平
    rx_done = Signal(modbv(0)[1:])
    rx_clk_cnt = Signal(modbv(0)[15 + 1 - 0:])
    rx_div_cnt = Signal(modbv(0)[15 + 1 - 0:])
    rx_data = Signal(modbv(0)[7 + 1 - 0:])
    rx_over = Signal(modbv(0)[1:])
    UART_CTRL = modbv(0x0)[8:]
    UART_STATUS = modbv(0x4)[8:]
    UART_BAUD = modbv(0x8)[8:]
    UART_TXDATA = modbv(0xc)[8:]
    UART_RXDATA = modbv(0x10)[8:]
    # addr: 0x00
    # rw. bit[0]: tx enable, 1 = enable, 0 = disable
    # rw. bit[1]: rx enable, 1 = enable, 0 = disable
    uart_ctrl = Signal(modbv(0)[31 + 1 - 0:])
    # addr: 0x04
    # ro. bit[0]: tx busy, 1 = busy, 0 = idle
    # rw. bit[1]: rx over, 1 = over, 0 = receiving
    # must check this bit before tx data
    uart_status = Signal(modbv(0)[31 + 1 - 0:])
    # addr: 0x08
    # rw. clk div
    uart_baud = Signal(modbv(0)[31 + 1 - 0:])
    # addr: 0x10
    # ro. rx data
    uart_rx = Signal(modbv(0)[31 + 1 - 0:])

    @always_comb
    def assign_0():
        tx_pin.next = tx_reg
    @always_comb
    def assign_1():
        # *************************** RX接收 ****************************
        # 下降沿检测(检测起始信号)
        rx_negedge.next = rx_q1 and not rx_q0
    # 写寄存器
    @always(clk.posedge)
    def seq_0():
        if rst == 0b0: 
            uart_ctrl.next = 0x0
            uart_status.next = 0x0
            uart_rx.next = 0x0
            uart_baud.next = BAUD_115200
            tx_data_valid.next = 0b0

        else:
            if we_i == 0b1:
                if addr_i[7 + 1:0] == UART_CTRL:
                    uart_ctrl.next = data_i
                elif addr_i[7 + 1:0] == UART_BAUD:
                    uart_baud.next = data_i
                elif addr_i[7 + 1:0] == UART_STATUS:
                    uart_status.next[1] = data_i[1]
                elif addr_i[7 + 1:0] == UART_TXDATA:
                    if uart_ctrl[0] == 0b1 and uart_status[0] == 0b0: 
                        tx_data.next = data_i[7 + 1:0]
                        uart_status.next[0] = 0b1
                        tx_data_valid.next = 0b1


            else: 
                tx_data_valid.next = 0b0
                if tx_data_ready == 0b1:
                    uart_status.next[0] = 0b0
                if uart_ctrl[1] == 0b1:
                    if rx_over == 0b1: 
                        uart_status.next[1] = 0b1
                        uart_rx.next = concat(modbv(0x0)[24:], rx_data)


    # 读寄存器
    @always_comb
    def comb_0():
        if rst == 0b0:
            data_o.next = 0x0
        else:
            if addr_i[7 + 1:0] == UART_CTRL:
                data_o.next = uart_ctrl
            elif addr_i[7 + 1:0] == UART_STATUS:
                data_o.next = uart_status
            elif addr_i[7 + 1:0] == UART_BAUD:
                data_o.next = uart_baud
            elif addr_i[7 + 1:0] == UART_RXDATA:
                data_o.next = uart_rx
            else:
                data_o.next = 0x0
    # *************************** TX发送 ****************************
    @always(clk.posedge)
    def seq_1():
        if rst == 0b0: 
            state.next = S_IDLE
            cycle_cnt.next = 0
            tx_reg.next = 0b0
            bit_cnt.next = 0
            tx_data_ready.next = 0b0

        else:
            if state == S_IDLE: 
                tx_reg.next = 0b1
                tx_data_ready.next = 0b0
                if tx_data_valid == 0b1: 
                    state.next = S_START
                    cycle_cnt.next = 0
                    bit_cnt.next = 0
                    tx_reg.next = 0b0


            else: 
                cycle_cnt.next = cycle_cnt + 1
                if cycle_cnt == uart_baud[15 + 1:0]: 
                    cycle_cnt.next = 0
                    if state == S_START: 
                        tx_reg.next = tx_data[bit_cnt]
                        state.next = S_SEND_BYTE
                        bit_cnt.next = bit_cnt + 1

                    elif state == S_SEND_BYTE: 
                        bit_cnt.next = bit_cnt + 1
                        if bit_cnt == 8: 
                            state.next = S_STOP
                            tx_reg.next = 0b1

                        else:
                            tx_reg.next = tx_data[bit_cnt]

                    elif state == S_STOP: 
                        tx_reg.next = 0b1
                        state.next = S_IDLE
                        tx_data_ready.next = 0b1




    @always(clk.posedge)
    def seq_2():
        if rst == 0b0: 
            rx_q0.next = 0b0
            rx_q1.next = 0b0

        else: 
            rx_q0.next = rx_pin
            rx_q1.next = rx_q0

    # 开始接收数据信号，接收期间一直有效
    @always(clk.posedge)
    def seq_3():
        if rst == 0b0:
            rx_start.next = 0b0
        else:
            if uart_ctrl[1]:
                if rx_negedge:
                    rx_start.next = 0b1
                elif rx_clk_edge_cnt == 9:
                    rx_start.next = 0b0
            else:
                rx_start.next = 0b0
    @always(clk.posedge)
    def seq_4():
        if rst == 0b0:
            rx_div_cnt.next = 0x0
        else:
            # 第一个时钟沿只需波特率分频系数的一半
            if rx_start == 0b1 and rx_clk_edge_cnt == 0x0:
                rx_div_cnt.next = concat(modbv(0b0)[1:], uart_baud[15 + 1:1])
            else:
                rx_div_cnt.next = uart_baud[15 + 1:0]
    # 对时钟进行计数
    @always(clk.posedge)
    def seq_5():
        if rst == 0b0:
            rx_clk_cnt.next = 0x0
        elif rx_start == 0b1:
            # 计数达到分频值
            if rx_clk_cnt == rx_div_cnt:
                rx_clk_cnt.next = 0x0
            else:
                rx_clk_cnt.next = rx_clk_cnt + 0b1
        else:
            rx_clk_cnt.next = 0x0
    # 每当时钟计数达到分频值时产生一个上升沿脉冲
    @always(clk.posedge)
    def seq_6():
        if rst == 0b0: 
            rx_clk_edge_cnt.next = 0x0
            rx_clk_edge_level.next = 0b0

        elif rx_start == 0b1:
            # 计数达到分频值
            if rx_clk_cnt == rx_div_cnt:
                # 时钟沿个数达到最大值
                if rx_clk_edge_cnt == 9: 
                    rx_clk_edge_cnt.next = 0x0
                    rx_clk_edge_level.next = 0b0

                else: 
                    # 时钟沿个数加1
                    rx_clk_edge_cnt.next = rx_clk_edge_cnt + 0b1
                    # 产生上升沿脉冲
                    rx_clk_edge_level.next = 0b1

            else:
                rx_clk_edge_level.next = 0b0
        else: 
            rx_clk_edge_cnt.next = 0x0
            rx_clk_edge_level.next = 0b0

    # bit序列
    @always(clk.posedge)
    def seq_7():
        if rst == 0b0: 
            rx_data.next = 0x0
            rx_over.next = 0b0

        else:
            if rx_start == 0b1:
                # 上升沿
                if rx_clk_edge_level == 0b1:
                    if rx_clk_edge_cnt == 1: 
                        pass

                    elif rx_clk_edge_cnt == 2: 
                        rx_data.next = rx_data | rx_pin << rx_clk_edge_cnt - 2
                        # 最后一位接收完成，置位接收完成标志
                        if rx_clk_edge_cnt == 0x9:
                            rx_over.next = 0b1

                    elif rx_clk_edge_cnt == 3: 
                        rx_data.next = rx_data | rx_pin << rx_clk_edge_cnt - 2
                        # 最后一位接收完成，置位接收完成标志
                        if rx_clk_edge_cnt == 0x9:
                            rx_over.next = 0b1

                    elif rx_clk_edge_cnt == 4: 
                        rx_data.next = rx_data | rx_pin << rx_clk_edge_cnt - 2
                        # 最后一位接收完成，置位接收完成标志
                        if rx_clk_edge_cnt == 0x9:
                            rx_over.next = 0b1

                    elif rx_clk_edge_cnt == 5: 
                        rx_data.next = rx_data | rx_pin << rx_clk_edge_cnt - 2
                        # 最后一位接收完成，置位接收完成标志
                        if rx_clk_edge_cnt == 0x9:
                            rx_over.next = 0b1

                    elif rx_clk_edge_cnt == 6: 
                        rx_data.next = rx_data | rx_pin << rx_clk_edge_cnt - 2
                        # 最后一位接收完成，置位接收完成标志
                        if rx_clk_edge_cnt == 0x9:
                            rx_over.next = 0b1

                    elif rx_clk_edge_cnt == 7: 
                        rx_data.next = rx_data | rx_pin << rx_clk_edge_cnt - 2
                        # 最后一位接收完成，置位接收完成标志
                        if rx_clk_edge_cnt == 0x9:
                            rx_over.next = 0b1

                    elif rx_clk_edge_cnt == 8: 
                        rx_data.next = rx_data | rx_pin << rx_clk_edge_cnt - 2
                        # 最后一位接收完成，置位接收完成标志
                        if rx_clk_edge_cnt == 0x9:
                            rx_over.next = 0b1

                    elif rx_clk_edge_cnt == 9: 
                        rx_data.next = rx_data | rx_pin << rx_clk_edge_cnt - 2
                        # 最后一位接收完成，置位接收完成标志
                        if rx_clk_edge_cnt == 0x9:
                            rx_over.next = 0b1


            else: 
                rx_data.next = 0x0
                rx_over.next = 0b0

    return instances()
