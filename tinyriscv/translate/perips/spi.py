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
# */ spi master模块
from myhdl import *

@block
def spi (
    clk,
    rst,
    data_i,
    addr_i,
    we_i,
    data_o,
    spi_mosi,
    # spi控制器输出、spi设备输入信号
    spi_miso,
    # spi控制器输入、spi设备输出信号
    spi_ss,
    # spi设备片选
    spi_clk
):
    SPI_CTRL = modbv(0x0)[4:]
    # spi_ctrl寄存器地址偏移
    # spi_ctrl寄存器地址偏移
    SPI_DATA = modbv(0x4)[4:]
    # spi_data寄存器地址偏移
    # spi_data寄存器地址偏移
    SPI_STATUS = modbv(0x8)[4:]
    # spi_status寄存器地址偏移
    # spi控制寄存器
    # addr: 0x00
    # [0]: 1: enable, 0: disable
    # [1]: CPOL
    # [2]: CPHA
    # [3]: select slave, 1: select, 0: deselect
    # [15:8]: clk div
    spi_ctrl = Signal(modbv(0)[31 + 1 - 0:])
    # spi数据寄存器
    # addr: 0x04
    # [7:0] cmd or inout data
    spi_data = Signal(modbv(0)[31 + 1 - 0:])
    # spi状态寄存器
    # addr: 0x08
    # [0]: 1: busy, 0: idle
    spi_status = Signal(modbv(0)[31 + 1 - 0:])
    clk_cnt = Signal(modbv(0)[8 + 1 - 0:])
    # 分频计数
    en = Signal(modbv(0)[1:])
    # 使能，开始传输信号，传输期间一直有效
    spi_clk_edge_cnt = Signal(modbv(0)[4 + 1 - 0:])
    # spi clk时钟沿的个数
    spi_clk_edge_level = Signal(modbv(0)[1:])
    # spi clk沿电平
    rdata = Signal(modbv(0)[7 + 1 - 0:])
    # 从spi设备读回来的数据
    done = Signal(modbv(0)[1:])
    # 传输完成信号
    bit_index = Signal(modbv(0)[3 + 1 - 0:])
    # 数据bit索引
    div_cnt = Signal(modbv(0)[8 + 1 - 0:])

    @always_comb
    def assign_0():
        spi_ss.next = ~spi_ctrl[3]
    @always_comb
    def assign_1():
        # SPI设备片选信号
        div_cnt.next = spi_ctrl[15 + 1:8]
    # 0: 2分频，1：4分频，2：8分频，3：16分频，4：32分频，以此类推
    # 产生使能信号
    # 传输期间一直有效
    @always(clk.posedge)
    def seq_0():
        if rst == 0b0:
            en.next = 0b0
        else:
            if spi_ctrl[0] == 0b1:
                en.next = 0b1
            elif done == 0b1:
                en.next = 0b0
            else:
                en.next = en
    # 对输入时钟进行计数
    @always(clk.posedge)
    def seq_1():
        if rst == 0b0:
            clk_cnt.next = 0x0
        elif en == 0b1:
            if clk_cnt == div_cnt:
                clk_cnt.next = 0x0
            else:
                clk_cnt.next = clk_cnt + 0b1
        else:
            clk_cnt.next = 0x0
    # 对spi clk沿进行计数
    # 每当计数到分频值时产生一个上升沿脉冲
    @always(clk.posedge)
    def seq_2():
        if rst == 0b0: 
            spi_clk_edge_cnt.next = 0x0
            spi_clk_edge_level.next = 0b0

        elif en == 0b1:
            # 计数达到分频值
            if clk_cnt == div_cnt:
                if spi_clk_edge_cnt == 17: 
                    spi_clk_edge_cnt.next = 0x0
                    spi_clk_edge_level.next = 0b0

                else: 
                    spi_clk_edge_cnt.next = spi_clk_edge_cnt + 0b1
                    spi_clk_edge_level.next = 0b1

            else:
                spi_clk_edge_level.next = 0b0
        else: 
            spi_clk_edge_cnt.next = 0x0
            spi_clk_edge_level.next = 0b0

    # bit序列
    @always(clk.posedge)
    def seq_3():
        if rst == 0b0: 
            spi_clk.next = 0b0
            rdata.next = 0x0
            spi_mosi.next = 0b0
            bit_index.next = 0x0

        else:
            if en:
                if spi_clk_edge_level == 0b1:
                    if spi_clk_edge_cnt == 1: 
                        spi_clk.next = ~spi_clk
                        if spi_ctrl[2] == 0b1: 
                            spi_mosi.next = spi_data[bit_index]
                            # 送出1bit数据
                            bit_index.next = bit_index - 0b1

                        else:
                            rdata.next = concat(rdata[6 + 1:0], spi_miso)

                    elif spi_clk_edge_cnt == 3: 
                        spi_clk.next = ~spi_clk
                        if spi_ctrl[2] == 0b1: 
                            spi_mosi.next = spi_data[bit_index]
                            # 送出1bit数据
                            bit_index.next = bit_index - 0b1

                        else:
                            rdata.next = concat(rdata[6 + 1:0], spi_miso)

                    elif spi_clk_edge_cnt == 5: 
                        spi_clk.next = ~spi_clk
                        if spi_ctrl[2] == 0b1: 
                            spi_mosi.next = spi_data[bit_index]
                            # 送出1bit数据
                            bit_index.next = bit_index - 0b1

                        else:
                            rdata.next = concat(rdata[6 + 1:0], spi_miso)

                    elif spi_clk_edge_cnt == 7: 
                        spi_clk.next = ~spi_clk
                        if spi_ctrl[2] == 0b1: 
                            spi_mosi.next = spi_data[bit_index]
                            # 送出1bit数据
                            bit_index.next = bit_index - 0b1

                        else:
                            rdata.next = concat(rdata[6 + 1:0], spi_miso)

                    elif spi_clk_edge_cnt == 9: 
                        spi_clk.next = ~spi_clk
                        if spi_ctrl[2] == 0b1: 
                            spi_mosi.next = spi_data[bit_index]
                            # 送出1bit数据
                            bit_index.next = bit_index - 0b1

                        else:
                            rdata.next = concat(rdata[6 + 1:0], spi_miso)

                    elif spi_clk_edge_cnt == 11: 
                        spi_clk.next = ~spi_clk
                        if spi_ctrl[2] == 0b1: 
                            spi_mosi.next = spi_data[bit_index]
                            # 送出1bit数据
                            bit_index.next = bit_index - 0b1

                        else:
                            rdata.next = concat(rdata[6 + 1:0], spi_miso)

                    elif spi_clk_edge_cnt == 13: 
                        spi_clk.next = ~spi_clk
                        if spi_ctrl[2] == 0b1: 
                            spi_mosi.next = spi_data[bit_index]
                            # 送出1bit数据
                            bit_index.next = bit_index - 0b1

                        else:
                            rdata.next = concat(rdata[6 + 1:0], spi_miso)

                    elif spi_clk_edge_cnt == 15: 
                        spi_clk.next = ~spi_clk
                        if spi_ctrl[2] == 0b1: 
                            spi_mosi.next = spi_data[bit_index]
                            # 送出1bit数据
                            bit_index.next = bit_index - 0b1

                        else:
                            rdata.next = concat(rdata[6 + 1:0], spi_miso)

                    elif spi_clk_edge_cnt == 2: 
                        spi_clk.next = ~spi_clk
                        if spi_ctrl[2] == 0b1:
                            rdata.next = concat(rdata[6 + 1:0], spi_miso)
                        else: 
                            spi_mosi.next = spi_data[bit_index]
                            # 送出1bit数据
                            bit_index.next = bit_index - 0b1


                    elif spi_clk_edge_cnt == 4: 
                        spi_clk.next = ~spi_clk
                        if spi_ctrl[2] == 0b1:
                            rdata.next = concat(rdata[6 + 1:0], spi_miso)
                        else: 
                            spi_mosi.next = spi_data[bit_index]
                            # 送出1bit数据
                            bit_index.next = bit_index - 0b1


                    elif spi_clk_edge_cnt == 6: 
                        spi_clk.next = ~spi_clk
                        if spi_ctrl[2] == 0b1:
                            rdata.next = concat(rdata[6 + 1:0], spi_miso)
                        else: 
                            spi_mosi.next = spi_data[bit_index]
                            # 送出1bit数据
                            bit_index.next = bit_index - 0b1


                    elif spi_clk_edge_cnt == 8: 
                        spi_clk.next = ~spi_clk
                        if spi_ctrl[2] == 0b1:
                            rdata.next = concat(rdata[6 + 1:0], spi_miso)
                        else: 
                            spi_mosi.next = spi_data[bit_index]
                            # 送出1bit数据
                            bit_index.next = bit_index - 0b1


                    elif spi_clk_edge_cnt == 10: 
                        spi_clk.next = ~spi_clk
                        if spi_ctrl[2] == 0b1:
                            rdata.next = concat(rdata[6 + 1:0], spi_miso)
                        else: 
                            spi_mosi.next = spi_data[bit_index]
                            # 送出1bit数据
                            bit_index.next = bit_index - 0b1


                    elif spi_clk_edge_cnt == 12: 
                        spi_clk.next = ~spi_clk
                        if spi_ctrl[2] == 0b1:
                            rdata.next = concat(rdata[6 + 1:0], spi_miso)
                        else: 
                            spi_mosi.next = spi_data[bit_index]
                            # 送出1bit数据
                            bit_index.next = bit_index - 0b1


                    elif spi_clk_edge_cnt == 14: 
                        spi_clk.next = ~spi_clk
                        if spi_ctrl[2] == 0b1:
                            rdata.next = concat(rdata[6 + 1:0], spi_miso)
                        else: 
                            spi_mosi.next = spi_data[bit_index]
                            # 送出1bit数据
                            bit_index.next = bit_index - 0b1


                    elif spi_clk_edge_cnt == 16: 
                        spi_clk.next = ~spi_clk
                        if spi_ctrl[2] == 0b1:
                            rdata.next = concat(rdata[6 + 1:0], spi_miso)
                        else: 
                            spi_mosi.next = spi_data[bit_index]
                            # 送出1bit数据
                            bit_index.next = bit_index - 0b1


                    elif spi_clk_edge_cnt == 17:
                        spi_clk.next = spi_ctrl[1]

            else: 
                # 初始状态
                spi_clk.next = spi_ctrl[1]
                if spi_ctrl[2] == 0b0: 
                    spi_mosi.next = spi_data[7]
                    # 送出最高位数据
                    bit_index.next = 0x6

                else:
                    bit_index.next = 0x7

    # 产生结束(完成)信号
    @always(clk.posedge)
    def seq_4():
        if rst == 0b0:
            done.next = 0b0
        else:
            if en and spi_clk_edge_cnt == 17:
                done.next = 0b1
            else:
                done.next = 0b0
    # write reg
    @always(clk.posedge)
    def seq_5():
        if rst == 0b0: 
            spi_ctrl.next = 0x0
            spi_data.next = 0x0
            spi_status.next = 0x0

        else: 
            spi_status.next[0] = en
            if we_i == 0b1:
                if addr_i[3 + 1:0] == SPI_CTRL:
                    spi_ctrl.next = data_i
                elif addr_i[3 + 1:0] == SPI_DATA:
                    spi_data.next = data_i
                else: 
                    pass

            else: 
                spi_ctrl.next[0] = 0b0
                # 发送完成后更新数据寄存器
                if done == 0b1:
                    spi_data.next = concat(modbv(0x0)[24:], rdata)


    # read reg
    @always_comb
    def comb_0():
        if rst == 0b0:
            data_o.next = 0x0
        else:
            if addr_i[3 + 1:0] == SPI_CTRL:
                data_o.next = spi_ctrl
            elif addr_i[3 + 1:0] == SPI_DATA:
                data_o.next = spi_data
            elif addr_i[3 + 1:0] == SPI_STATUS:
                data_o.next = spi_status
            else:
                data_o.next = 0x0
    return instances()
