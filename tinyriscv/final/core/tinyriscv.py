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
# tinyriscv处理器核顶层模块
from core.clint import *
from core.pc_reg import *
from core.regs import *
from core.ctrl import *
from core.csr_reg import *
from core.if_id import *
from core.id_ex import *
from core.id import *
from core.ex import *
from core.div import *


@block
def tinyriscv (
    clk,
    rst,
    rib_ex_addr_o,
    # 读、写外设的地址
    rib_ex_data_i,
    # 从外设读取的数据
    rib_ex_data_o,
    # 写入外设的数据
    rib_ex_req_o,
    # 访问外设请求
    rib_ex_we_o,
    # 写外设标志
    rib_pc_addr_o,
    # 取指地址
    rib_pc_data_i,
    # 取到的指令内容
    jtag_reg_addr_i,
    # jtag模块读、写寄存器的地址
    jtag_reg_data_i,
    # jtag模块写寄存器数据
    jtag_reg_we_i,
    # jtag模块写寄存器标志
    jtag_reg_data_o,
    # jtag模块读取到的寄存器数据
    rib_hold_flag_i,
    # 总线暂停标志
    jtag_halt_flag_i,
    # jtag暂停标志
    jtag_reset_flag_i,
    # jtag复位PC标志
    int_i
):
    # pc_reg模块输出信号
    pc_pc_o = Signal(modbv(0)[31 + 1 - 0:])
    # if_id模块输出信号
    if_inst_o = Signal(modbv(0)[31 + 1 - 0:])
    if_inst_addr_o = Signal(modbv(0)[31 + 1 - 0:])
    if_int_flag_o = Signal(modbv(0)[7 + 1 - 0:])
    # id模块输出信号
    id_reg1_raddr_o = Signal(modbv(0)[4 + 1 - 0:])
    id_reg2_raddr_o = Signal(modbv(0)[4 + 1 - 0:])
    id_inst_o = Signal(modbv(0)[31 + 1 - 0:])
    id_inst_addr_o = Signal(modbv(0)[31 + 1 - 0:])
    id_reg1_rdata_o = Signal(modbv(0)[31 + 1 - 0:])
    id_reg2_rdata_o = Signal(modbv(0)[31 + 1 - 0:])
    id_reg_we_o = Signal(modbv(0)[1:])
    id_reg_waddr_o = Signal(modbv(0)[4 + 1 - 0:])
    id_csr_raddr_o = Signal(modbv(0)[31 + 1 - 0:])
    id_csr_we_o = Signal(modbv(0)[1:])
    id_csr_rdata_o = Signal(modbv(0)[31 + 1 - 0:])
    id_csr_waddr_o = Signal(modbv(0)[31 + 1 - 0:])
    id_op1_o = Signal(modbv(0)[31 + 1 - 0:])
    id_op2_o = Signal(modbv(0)[31 + 1 - 0:])
    id_op1_jump_o = Signal(modbv(0)[31 + 1 - 0:])
    id_op2_jump_o = Signal(modbv(0)[31 + 1 - 0:])
    # id_ex模块输出信号
    ie_inst_o = Signal(modbv(0)[31 + 1 - 0:])
    ie_inst_addr_o = Signal(modbv(0)[31 + 1 - 0:])
    ie_reg_we_o = Signal(modbv(0)[1:])
    ie_reg_waddr_o = Signal(modbv(0)[4 + 1 - 0:])
    ie_reg1_rdata_o = Signal(modbv(0)[31 + 1 - 0:])
    ie_reg2_rdata_o = Signal(modbv(0)[31 + 1 - 0:])
    ie_csr_we_o = Signal(modbv(0)[1:])
    ie_csr_waddr_o = Signal(modbv(0)[31 + 1 - 0:])
    ie_csr_rdata_o = Signal(modbv(0)[31 + 1 - 0:])
    ie_op1_o = Signal(modbv(0)[31 + 1 - 0:])
    ie_op2_o = Signal(modbv(0)[31 + 1 - 0:])
    ie_op1_jump_o = Signal(modbv(0)[31 + 1 - 0:])
    ie_op2_jump_o = Signal(modbv(0)[31 + 1 - 0:])
    # ex模块输出信号
    ex_mem_wdata_o = Signal(modbv(0)[31 + 1 - 0:])
    ex_mem_raddr_o = Signal(modbv(0)[31 + 1 - 0:])
    ex_mem_waddr_o = Signal(modbv(0)[31 + 1 - 0:])
    ex_mem_we_o = Signal(modbv(0)[1:])
    ex_mem_req_o = Signal(modbv(0)[1:])
    ex_reg_wdata_o = Signal(modbv(0)[31 + 1 - 0:])
    ex_reg_we_o = Signal(modbv(0)[1:])
    ex_reg_waddr_o = Signal(modbv(0)[4 + 1 - 0:])
    ex_hold_flag_o = Signal(modbv(0)[1:])
    ex_jump_flag_o = Signal(modbv(0)[1:])
    ex_jump_addr_o = Signal(modbv(0)[31 + 1 - 0:])
    ex_div_start_o = Signal(modbv(0)[1:])
    ex_div_dividend_o = Signal(modbv(0)[31 + 1 - 0:])
    ex_div_divisor_o = Signal(modbv(0)[31 + 1 - 0:])
    ex_div_op_o = Signal(modbv(0)[2 + 1 - 0:])
    ex_div_reg_waddr_o = Signal(modbv(0)[4 + 1 - 0:])
    ex_csr_wdata_o = Signal(modbv(0)[31 + 1 - 0:])
    ex_csr_we_o = Signal(modbv(0)[1:])
    ex_csr_waddr_o = Signal(modbv(0)[31 + 1 - 0:])
    # regs模块输出信号
    regs_rdata1_o = Signal(modbv(0)[31 + 1 - 0:])
    regs_rdata2_o = Signal(modbv(0)[31 + 1 - 0:])
    # csr_reg模块输出信号
    csr_data_o = Signal(modbv(0)[31 + 1 - 0:])
    csr_clint_data_o = Signal(modbv(0)[31 + 1 - 0:])
    csr_global_int_en_o = Signal(modbv(0)[1:])
    csr_clint_csr_mtvec = Signal(modbv(0)[31 + 1 - 0:])
    csr_clint_csr_mepc = Signal(modbv(0)[31 + 1 - 0:])
    csr_clint_csr_mstatus = Signal(modbv(0)[31 + 1 - 0:])
    # ctrl模块输出信号
    ctrl_hold_flag_o = Signal(modbv(0)[2 + 1 - 0:])
    ctrl_jump_flag_o = Signal(modbv(0)[1:])
    ctrl_jump_addr_o = Signal(modbv(0)[31 + 1 - 0:])
    # div模块输出信号
    div_result_o = Signal(modbv(0)[31 + 1 - 0:])
    div_ready_o = Signal(modbv(0)[1:])
    div_busy_o = Signal(modbv(0)[1:])
    div_reg_waddr_o = Signal(modbv(0)[4 + 1 - 0:])
    # clint模块输出信号
    clint_we_o = Signal(modbv(0)[1:])
    clint_waddr_o = Signal(modbv(0)[31 + 1 - 0:])
    clint_raddr_o = Signal(modbv(0)[31 + 1 - 0:])
    clint_data_o = Signal(modbv(0)[31 + 1 - 0:])
    clint_int_addr_o = Signal(modbv(0)[31 + 1 - 0:])
    clint_int_assert_o = Signal(modbv(0)[1:])
    clint_hold_flag_o = Signal(modbv(0)[1:])

    @always_comb
    def assign_0():
        rib_ex_addr_o.next = ex_mem_waddr_o if (ex_mem_we_o == 0b1) else ex_mem_raddr_o
    @always_comb
    def assign_1():
        rib_ex_data_o.next = ex_mem_wdata_o
    @always_comb
    def assign_2():
        rib_ex_req_o.next = ex_mem_req_o
    @always_comb
    def assign_3():
        rib_ex_we_o.next = ex_mem_we_o
    @always_comb
    def assign_4():
        rib_pc_addr_o.next = pc_pc_o
    u_pc_reg = pc_reg(
        clk=clk,
        rst=rst,
        jtag_reset_flag_i=jtag_reset_flag_i,
        pc_o=pc_pc_o,
        hold_flag_i=ctrl_hold_flag_o,
        jump_flag_i=ctrl_jump_flag_o,
        jump_addr_i=ctrl_jump_addr_o
    )
    u_ctrl = ctrl(
        rst=rst,
        jump_flag_i=ex_jump_flag_o,
        jump_addr_i=ex_jump_addr_o,
        hold_flag_ex_i=ex_hold_flag_o,
        hold_flag_rib_i=rib_hold_flag_i,
        hold_flag_o=ctrl_hold_flag_o,
        hold_flag_clint_i=clint_hold_flag_o,
        jump_flag_o=ctrl_jump_flag_o,
        jump_addr_o=ctrl_jump_addr_o,
        jtag_halt_flag_i=jtag_halt_flag_i
    )
    u_regs = regs(
        clk=clk,
        rst=rst,
        we_i=ex_reg_we_o,
        waddr_i=ex_reg_waddr_o,
        wdata_i=ex_reg_wdata_o,
        raddr1_i=id_reg1_raddr_o,
        rdata1_o=regs_rdata1_o,
        raddr2_i=id_reg2_raddr_o,
        rdata2_o=regs_rdata2_o,
        jtag_we_i=jtag_reg_we_i,
        jtag_addr_i=jtag_reg_addr_i,
        jtag_data_i=jtag_reg_data_i,
        jtag_data_o=jtag_reg_data_o
    )
    u_csr_reg = csr_reg(
        clk=clk,
        rst=rst,
        we_i=ex_csr_we_o,
        raddr_i=id_csr_raddr_o,
        waddr_i=ex_csr_waddr_o,
        data_i=ex_csr_wdata_o,
        data_o=csr_data_o,
        global_int_en_o=csr_global_int_en_o,
        clint_we_i=clint_we_o,
        clint_raddr_i=clint_raddr_o,
        clint_waddr_i=clint_waddr_o,
        clint_data_i=clint_data_o,
        clint_data_o=csr_clint_data_o,
        clint_csr_mtvec=csr_clint_csr_mtvec,
        clint_csr_mepc=csr_clint_csr_mepc,
        clint_csr_mstatus=csr_clint_csr_mstatus
    )
    u_if_id = if_id(
        clk=clk,
        rst=rst,
        inst_i=rib_pc_data_i,
        inst_addr_i=pc_pc_o,
        int_flag_i=int_i,
        int_flag_o=if_int_flag_o,
        hold_flag_i=ctrl_hold_flag_o,
        inst_o=if_inst_o,
        inst_addr_o=if_inst_addr_o
    )
    u_id = id(
        rst=rst,
        inst_i=if_inst_o,
        inst_addr_i=if_inst_addr_o,
        reg1_rdata_i=regs_rdata1_o,
        reg2_rdata_i=regs_rdata2_o,
        ex_jump_flag_i=ex_jump_flag_o,
        reg1_raddr_o=id_reg1_raddr_o,
        reg2_raddr_o=id_reg2_raddr_o,
        inst_o=id_inst_o,
        inst_addr_o=id_inst_addr_o,
        reg1_rdata_o=id_reg1_rdata_o,
        reg2_rdata_o=id_reg2_rdata_o,
        reg_we_o=id_reg_we_o,
        reg_waddr_o=id_reg_waddr_o,
        op1_o=id_op1_o,
        op2_o=id_op2_o,
        op1_jump_o=id_op1_jump_o,
        op2_jump_o=id_op2_jump_o,
        csr_rdata_i=csr_data_o,
        csr_raddr_o=id_csr_raddr_o,
        csr_we_o=id_csr_we_o,
        csr_rdata_o=id_csr_rdata_o,
        csr_waddr_o=id_csr_waddr_o
    )
    u_id_ex = id_ex(
        clk=clk,
        rst=rst,
        inst_i=id_inst_o,
        inst_addr_i=id_inst_addr_o,
        reg_we_i=id_reg_we_o,
        reg_waddr_i=id_reg_waddr_o,
        reg1_rdata_i=id_reg1_rdata_o,
        reg2_rdata_i=id_reg2_rdata_o,
        hold_flag_i=ctrl_hold_flag_o,
        inst_o=ie_inst_o,
        inst_addr_o=ie_inst_addr_o,
        reg_we_o=ie_reg_we_o,
        reg_waddr_o=ie_reg_waddr_o,
        reg1_rdata_o=ie_reg1_rdata_o,
        reg2_rdata_o=ie_reg2_rdata_o,
        op1_i=id_op1_o,
        op2_i=id_op2_o,
        op1_jump_i=id_op1_jump_o,
        op2_jump_i=id_op2_jump_o,
        op1_o=ie_op1_o,
        op2_o=ie_op2_o,
        op1_jump_o=ie_op1_jump_o,
        op2_jump_o=ie_op2_jump_o,
        csr_we_i=id_csr_we_o,
        csr_waddr_i=id_csr_waddr_o,
        csr_rdata_i=id_csr_rdata_o,
        csr_we_o=ie_csr_we_o,
        csr_waddr_o=ie_csr_waddr_o,
        csr_rdata_o=ie_csr_rdata_o
    )
    u_ex = ex(
        rst=rst,
        inst_i=ie_inst_o,
        inst_addr_i=ie_inst_addr_o,
        reg_we_i=ie_reg_we_o,
        reg_waddr_i=ie_reg_waddr_o,
        reg1_rdata_i=ie_reg1_rdata_o,
        reg2_rdata_i=ie_reg2_rdata_o,
        op1_i=ie_op1_o,
        op2_i=ie_op2_o,
        op1_jump_i=ie_op1_jump_o,
        op2_jump_i=ie_op2_jump_o,
        mem_rdata_i=rib_ex_data_i,
        mem_wdata_o=ex_mem_wdata_o,
        mem_raddr_o=ex_mem_raddr_o,
        mem_waddr_o=ex_mem_waddr_o,
        mem_we_o=ex_mem_we_o,
        mem_req_o=ex_mem_req_o,
        reg_wdata_o=ex_reg_wdata_o,
        reg_we_o=ex_reg_we_o,
        reg_waddr_o=ex_reg_waddr_o,
        hold_flag_o=ex_hold_flag_o,
        jump_flag_o=ex_jump_flag_o,
        jump_addr_o=ex_jump_addr_o,
        int_assert_i=clint_int_assert_o,
        int_addr_i=clint_int_addr_o,
        div_ready_i=div_ready_o,
        div_result_i=div_result_o,
        div_busy_i=div_busy_o,
        div_reg_waddr_i=div_reg_waddr_o,
        div_start_o=ex_div_start_o,
        div_dividend_o=ex_div_dividend_o,
        div_divisor_o=ex_div_divisor_o,
        div_op_o=ex_div_op_o,
        div_reg_waddr_o=ex_div_reg_waddr_o,
        csr_we_i=ie_csr_we_o,
        csr_waddr_i=ie_csr_waddr_o,
        csr_rdata_i=ie_csr_rdata_o,
        csr_wdata_o=ex_csr_wdata_o,
        csr_we_o=ex_csr_we_o,
        csr_waddr_o=ex_csr_waddr_o
    )
    u_div = div(
        clk=clk,
        rst=rst,
        dividend_i=ex_div_dividend_o,
        divisor_i=ex_div_divisor_o,
        start_i=ex_div_start_o,
        op_i=ex_div_op_o,
        reg_waddr_i=ex_div_reg_waddr_o,
        result_o=div_result_o,
        ready_o=div_ready_o,
        busy_o=div_busy_o,
        reg_waddr_o=div_reg_waddr_o
    )
    u_clint = clint(
        clk=clk,
        rst=rst,
        int_flag_i=if_int_flag_o,
        inst_i=id_inst_o,
        inst_addr_i=id_inst_addr_o,
        jump_flag_i=ex_jump_flag_o,
        jump_addr_i=ex_jump_addr_o,
        hold_flag_i=ctrl_hold_flag_o,
        div_started_i=ex_div_start_o,
        data_i=csr_clint_data_o,
        csr_mtvec=csr_clint_csr_mtvec,
        csr_mepc=csr_clint_csr_mepc,
        csr_mstatus=csr_clint_csr_mstatus,
        we_o=clint_we_o,
        waddr_o=clint_waddr_o,
        raddr_o=clint_raddr_o,
        data_o=clint_data_o,
        hold_flag_o=clint_hold_flag_o,
        global_int_en_i=csr_global_int_en_o,
        int_addr_o=clint_int_addr_o,
        int_assert_o=clint_int_assert_o
    )
    return instances()
