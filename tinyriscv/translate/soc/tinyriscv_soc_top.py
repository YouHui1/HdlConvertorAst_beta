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
# tinyriscv soc顶层模块
from myhdl import *

@block
def tinyriscv_soc_top (
    clk,
    rst,
    over,
    # 测试是否完成信号
    succ,
    # 测试是否成功信号
    halted_ind,
    # jtag是否已经halt住CPU信号
    uart_debug_pin,
    # 串口下载使能引脚
    uart_tx_pin,
    # UART发送引脚
    uart_rx_pin,
    # UART接收引脚
    gpio,
    # GPIO引脚
    jtag_TCK,
    # JTAG TCK引脚
    jtag_TMS,
    # JTAG TMS引脚
    jtag_TDI,
    # JTAG TDI引脚
    jtag_TDO,
    # JTAG TDO引脚
    spi_miso,
    # SPI MISO引脚
    spi_mosi,
    # SPI MOSI引脚
    spi_ss,
    # SPI SS引脚
    spi_clk
):
    # master 0 interface
    m0_addr_i = Signal(modbv(0)[31 + 1 - 0:])
    m0_data_i = Signal(modbv(0)[31 + 1 - 0:])
    m0_data_o = Signal(modbv(0)[31 + 1 - 0:])
    m0_req_i = Signal(modbv(0)[1:])
    m0_we_i = Signal(modbv(0)[1:])
    # master 1 interface
    m1_addr_i = Signal(modbv(0)[31 + 1 - 0:])
    m1_data_i = Signal(modbv(0)[31 + 1 - 0:])
    m1_data_o = Signal(modbv(0)[31 + 1 - 0:])
    m1_req_i = Signal(modbv(0)[1:])
    m1_we_i = Signal(modbv(0)[1:])
    # master 2 interface
    m2_addr_i = Signal(modbv(0)[31 + 1 - 0:])
    m2_data_i = Signal(modbv(0)[31 + 1 - 0:])
    m2_data_o = Signal(modbv(0)[31 + 1 - 0:])
    m2_req_i = Signal(modbv(0)[1:])
    m2_we_i = Signal(modbv(0)[1:])
    # master 3 interface
    m3_addr_i = Signal(modbv(0)[31 + 1 - 0:])
    m3_data_i = Signal(modbv(0)[31 + 1 - 0:])
    m3_data_o = Signal(modbv(0)[31 + 1 - 0:])
    m3_req_i = Signal(modbv(0)[1:])
    m3_we_i = Signal(modbv(0)[1:])
    # slave 0 interface
    s0_addr_o = Signal(modbv(0)[31 + 1 - 0:])
    s0_data_o = Signal(modbv(0)[31 + 1 - 0:])
    s0_data_i = Signal(modbv(0)[31 + 1 - 0:])
    s0_we_o = Signal(modbv(0)[1:])
    # slave 1 interface
    s1_addr_o = Signal(modbv(0)[31 + 1 - 0:])
    s1_data_o = Signal(modbv(0)[31 + 1 - 0:])
    s1_data_i = Signal(modbv(0)[31 + 1 - 0:])
    s1_we_o = Signal(modbv(0)[1:])
    # slave 2 interface
    s2_addr_o = Signal(modbv(0)[31 + 1 - 0:])
    s2_data_o = Signal(modbv(0)[31 + 1 - 0:])
    s2_data_i = Signal(modbv(0)[31 + 1 - 0:])
    s2_we_o = Signal(modbv(0)[1:])
    # slave 3 interface
    s3_addr_o = Signal(modbv(0)[31 + 1 - 0:])
    s3_data_o = Signal(modbv(0)[31 + 1 - 0:])
    s3_data_i = Signal(modbv(0)[31 + 1 - 0:])
    s3_we_o = Signal(modbv(0)[1:])
    # slave 4 interface
    s4_addr_o = Signal(modbv(0)[31 + 1 - 0:])
    s4_data_o = Signal(modbv(0)[31 + 1 - 0:])
    s4_data_i = Signal(modbv(0)[31 + 1 - 0:])
    s4_we_o = Signal(modbv(0)[1:])
    # slave 5 interface
    s5_addr_o = Signal(modbv(0)[31 + 1 - 0:])
    s5_data_o = Signal(modbv(0)[31 + 1 - 0:])
    s5_data_i = Signal(modbv(0)[31 + 1 - 0:])
    s5_we_o = Signal(modbv(0)[1:])
    # rib
    rib_hold_flag_o = Signal(modbv(0)[1:])
    # jtag
    jtag_halt_req_o = Signal(modbv(0)[1:])
    jtag_reset_req_o = Signal(modbv(0)[1:])
    jtag_reg_addr_o = Signal(modbv(0)[4 + 1 - 0:])
    jtag_reg_data_o = Signal(modbv(0)[31 + 1 - 0:])
    jtag_reg_we_o = Signal(modbv(0)[1:])
    jtag_reg_data_i = Signal(modbv(0)[31 + 1 - 0:])
    # tinyriscv
    int_flag = Signal(modbv(0)[7 + 1 - 0:])
    # timer0
    timer0_int = Signal(modbv(0)[1:])
    # gpio
    io_in = Signal(modbv(0)[1 + 1 - 0:])
    gpio_ctrl = Signal(modbv(0)[31 + 1 - 0:])
    gpio_data = Signal(modbv(0)[31 + 1 - 0:])

    @always_comb
    def assign_0():
        int_flag.next = concat(modbv(0x0)[7:], timer0_int)
    @always_comb
    def assign_1():
        # 低电平点亮LED
        # 低电平表示已经halt住CPU
        halted_ind.next = ~jtag_halt_req_o
    @always(clk.posedge)
    def seq_0():
        if rst == 0b0: 
            over.next = 0b1
            succ.next = 0b1

        else: 
            over.next = ~u_tinyriscv.u_regs.regs[26]
            # when = 1, run over
            succ.next = ~u_tinyriscv.u_regs.regs[27]

    u_rib = rib(
        clk=clk,
        rst=rst,
        m0_addr_i=m0_addr_i,
        m0_data_i=m0_data_i,
        m0_data_o=m0_data_o,
        m0_req_i=m0_req_i,
        m0_we_i=m0_we_i,
        m1_addr_i=m1_addr_i,
        m1_data_i=Signal(modbv(0x0)[31 + 1 - 0:]),
        m1_data_o=m1_data_o,
        m1_req_i=Signal(modbv(0b1)[1:]),
        m1_we_i=Signal(modbv(0b0)[1:]),
        m2_addr_i=m2_addr_i,
        m2_data_i=m2_data_i,
        m2_data_o=m2_data_o,
        m2_req_i=m2_req_i,
        m2_we_i=m2_we_i,
        m3_addr_i=m3_addr_i,
        m3_data_i=m3_data_i,
        m3_data_o=m3_data_o,
        m3_req_i=m3_req_i,
        m3_we_i=m3_we_i,
        s0_addr_o=s0_addr_o,
        s0_data_o=s0_data_o,
        s0_data_i=s0_data_i,
        s0_we_o=s0_we_o,
        s1_addr_o=s1_addr_o,
        s1_data_o=s1_data_o,
        s1_data_i=s1_data_i,
        s1_we_o=s1_we_o,
        s2_addr_o=s2_addr_o,
        s2_data_o=s2_data_o,
        s2_data_i=s2_data_i,
        s2_we_o=s2_we_o,
        s3_addr_o=s3_addr_o,
        s3_data_o=s3_data_o,
        s3_data_i=s3_data_i,
        s3_we_o=s3_we_o,
        s4_addr_o=s4_addr_o,
        s4_data_o=s4_data_o,
        s4_data_i=s4_data_i,
        s4_we_o=s4_we_o,
        s5_addr_o=s5_addr_o,
        s5_data_o=s5_data_o,
        s5_data_i=s5_data_i,
        s5_we_o=s5_we_o,
        hold_flag_o=rib_hold_flag_o
    )
    u_tinyriscv = tinyriscv(
        clk=clk,
        rst=rst,
        rib_ex_addr_o=m0_addr_i,
        rib_ex_data_i=m0_data_o,
        rib_ex_data_o=m0_data_i,
        rib_ex_req_o=m0_req_i,
        rib_ex_we_o=m0_we_i,
        rib_pc_addr_o=m1_addr_i,
        rib_pc_data_i=m1_data_o,
        jtag_reg_addr_i=jtag_reg_addr_o,
        jtag_reg_data_i=jtag_reg_data_o,
        jtag_reg_we_i=jtag_reg_we_o,
        jtag_reg_data_o=jtag_reg_data_i,
        rib_hold_flag_i=rib_hold_flag_o,
        jtag_halt_flag_i=jtag_halt_req_o,
        jtag_reset_flag_i=jtag_reset_req_o,
        int_i=int_flag
    )
    u_rom = rom(
        clk=clk,
        rst=rst,
        we_i=s0_we_o,
        addr_i=s0_addr_o,
        data_i=s0_data_o,
        data_o=s0_data_i
    )
    return instances()
