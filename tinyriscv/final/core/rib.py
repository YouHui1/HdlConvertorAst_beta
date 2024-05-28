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
# RIB总线模块
from myhdl import *

@block
def rib (
    clk,
    rst,
    # master 0 interface
    m0_addr_i,
    # 主设备0读、写地址
    m0_data_i,
    # 主设备0写数据
    m0_data_o,
    # 主设备0读取到的数据
    m0_req_i,
    # 主设备0访问请求标志
    m0_we_i,
    # 主设备0写标志
    # master 1 interface
    m1_addr_i,
    # 主设备1读、写地址
    m1_data_i,
    # 主设备1写数据
    m1_data_o,
    # 主设备1读取到的数据
    m1_req_i,
    # 主设备1访问请求标志
    m1_we_i,
    # 主设备1写标志
    # master 2 interface
    m2_addr_i,
    # 主设备2读、写地址
    m2_data_i,
    # 主设备2写数据
    m2_data_o,
    # 主设备2读取到的数据
    m2_req_i,
    # 主设备2访问请求标志
    m2_we_i,
    # 主设备2写标志
    # master 3 interface
    m3_addr_i,
    # 主设备3读、写地址
    m3_data_i,
    # 主设备3写数据
    m3_data_o,
    # 主设备3读取到的数据
    m3_req_i,
    # 主设备3访问请求标志
    m3_we_i,
    # 主设备3写标志
    # slave 0 interface
    s0_addr_o,
    # 从设备0读、写地址
    s0_data_o,
    # 从设备0写数据
    s0_data_i,
    # 从设备0读取到的数据
    s0_we_o,
    # 从设备0写标志
    # slave 1 interface
    s1_addr_o,
    # 从设备1读、写地址
    s1_data_o,
    # 从设备1写数据
    s1_data_i,
    # 从设备1读取到的数据
    s1_we_o,
    # 从设备1写标志
    # slave 2 interface
    s2_addr_o,
    # 从设备2读、写地址
    s2_data_o,
    # 从设备2写数据
    s2_data_i,
    # 从设备2读取到的数据
    s2_we_o,
    # 从设备2写标志
    # slave 3 interface
    s3_addr_o,
    # 从设备3读、写地址
    s3_data_o,
    # 从设备3写数据
    s3_data_i,
    # 从设备3读取到的数据
    s3_we_o,
    # 从设备3写标志
    # slave 4 interface
    s4_addr_o,
    # 从设备4读、写地址
    s4_data_o,
    # 从设备4写数据
    s4_data_i,
    # 从设备4读取到的数据
    s4_we_o,
    # 从设备4写标志
    # slave 5 interface
    s5_addr_o,
    # 从设备5读、写地址
    s5_data_o,
    # 从设备5写数据
    s5_data_i,
    # 从设备5读取到的数据
    s5_we_o,
    # 从设备5写标志
    hold_flag_o,
    # 访问地址的最高4位决定要访问的是哪一个从设备
    # 因此最多支持16个从设备
    slave_0 = 0b0000,
    slave_1 = 0b0001,
    slave_2 = 0b0010,
    slave_3 = 0b0011,
    slave_4 = 0b0100,
    slave_5 = 0b0101,
    grant0 = 0x0,
    grant1 = 0x1,
    grant2 = 0x2,
    grant3 = 0x3
):
    req = Signal(modbv(0)[3 + 1 - 0:])
    grant = Signal(modbv(0)[1 + 1 - 0:])

    @always_comb
    def assign_0():
        # 主设备请求信号
        req.next = concat(concat(concat(m3_req_i, m2_req_i), m1_req_i), m0_req_i)
    # 仲裁逻辑
    # 固定优先级仲裁机制
    # 优先级由高到低：主设备3，主设备0，主设备2，主设备1
    @always_comb
    def comb_0():
        if req[3]:
            grant.next = grant3
            hold_flag_o.next = 0b1

        elif req[0]:
            grant.next = grant0
            hold_flag_o.next = 0b1

        elif req[2]:
            grant.next = grant2
            hold_flag_o.next = 0b1

        else:
            grant.next = grant1
            hold_flag_o.next = 0b0

    # 根据仲裁结果，选择(访问)对应的从设备
    @always_comb
    def comb_1():
        m0_data_o.next = 0x0
        m1_data_o.next = 0x00000001
        m2_data_o.next = 0x0
        m3_data_o.next = 0x0
        s0_addr_o.next = 0x0
        s1_addr_o.next = 0x0
        s2_addr_o.next = 0x0
        s3_addr_o.next = 0x0
        s4_addr_o.next = 0x0
        s5_addr_o.next = 0x0
        s0_data_o.next = 0x0
        s1_data_o.next = 0x0
        s2_data_o.next = 0x0
        s3_data_o.next = 0x0
        s4_data_o.next = 0x0
        s5_data_o.next = 0x0
        s0_we_o.next = 0b0
        s1_we_o.next = 0b0
        s2_we_o.next = 0b0
        s3_we_o.next = 0b0
        s4_we_o.next = 0b0
        s5_we_o.next = 0b0
        if grant == grant0:
            if m0_addr_i[31 + 1:28] == slave_0:
                s0_we_o.next = m0_we_i
                s0_addr_o.next = concat(modbv(0x0)[4:], m0_addr_i[27 + 1:0])
                s0_data_o.next = m0_data_i
                m0_data_o.next = s0_data_i

            elif m0_addr_i[31 + 1:28] == slave_1:
                s1_we_o.next = m0_we_i
                s1_addr_o.next = concat(modbv(0x0)[4:], m0_addr_i[27 + 1:0])
                s1_data_o.next = m0_data_i
                m0_data_o.next = s1_data_i

            elif m0_addr_i[31 + 1:28] == slave_2:
                s2_we_o.next = m0_we_i
                s2_addr_o.next = concat(modbv(0x0)[4:], m0_addr_i[27 + 1:0])
                s2_data_o.next = m0_data_i
                m0_data_o.next = s2_data_i

            elif m0_addr_i[31 + 1:28] == slave_3:
                s3_we_o.next = m0_we_i
                s3_addr_o.next = concat(modbv(0x0)[4:], m0_addr_i[27 + 1:0])
                s3_data_o.next = m0_data_i
                m0_data_o.next = s3_data_i

            elif m0_addr_i[31 + 1:28] == slave_4:
                s4_we_o.next = m0_we_i
                s4_addr_o.next = concat(modbv(0x0)[4:], m0_addr_i[27 + 1:0])
                s4_data_o.next = m0_data_i
                m0_data_o.next = s4_data_i

            elif m0_addr_i[31 + 1:28] == slave_5:
                s5_we_o.next = m0_we_i
                s5_addr_o.next = concat(modbv(0x0)[4:], m0_addr_i[27 + 1:0])
                s5_data_o.next = m0_data_i
                m0_data_o.next = s5_data_i

            else:
                pass

        elif grant == grant1:
            if m1_addr_i[31 + 1:28] == slave_0:
                s0_we_o.next = m1_we_i
                s0_addr_o.next = concat(modbv(0x0)[4:], m1_addr_i[27 + 1:0])
                s0_data_o.next = m1_data_i
                m1_data_o.next = s0_data_i

            elif m1_addr_i[31 + 1:28] == slave_1:
                s1_we_o.next = m1_we_i
                s1_addr_o.next = concat(modbv(0x0)[4:], m1_addr_i[27 + 1:0])
                s1_data_o.next = m1_data_i
                m1_data_o.next = s1_data_i

            elif m1_addr_i[31 + 1:28] == slave_2:
                s2_we_o.next = m1_we_i
                s2_addr_o.next = concat(modbv(0x0)[4:], m1_addr_i[27 + 1:0])
                s2_data_o.next = m1_data_i
                m1_data_o.next = s2_data_i

            elif m1_addr_i[31 + 1:28] == slave_3:
                s3_we_o.next = m1_we_i
                s3_addr_o.next = concat(modbv(0x0)[4:], m1_addr_i[27 + 1:0])
                s3_data_o.next = m1_data_i
                m1_data_o.next = s3_data_i

            elif m1_addr_i[31 + 1:28] == slave_4:
                s4_we_o.next = m1_we_i
                s4_addr_o.next = concat(modbv(0x0)[4:], m1_addr_i[27 + 1:0])
                s4_data_o.next = m1_data_i
                m1_data_o.next = s4_data_i

            elif m1_addr_i[31 + 1:28] == slave_5:
                s5_we_o.next = m1_we_i
                s5_addr_o.next = concat(modbv(0x0)[4:], m1_addr_i[27 + 1:0])
                s5_data_o.next = m1_data_i
                m1_data_o.next = s5_data_i

            else:
                pass

        elif grant == grant2:
            if m2_addr_i[31 + 1:28] == slave_0:
                s0_we_o.next = m2_we_i
                s0_addr_o.next = concat(modbv(0x0)[4:], m2_addr_i[27 + 1:0])
                s0_data_o.next = m2_data_i
                m2_data_o.next = s0_data_i

            elif m2_addr_i[31 + 1:28] == slave_1:
                s1_we_o.next = m2_we_i
                s1_addr_o.next = concat(modbv(0x0)[4:], m2_addr_i[27 + 1:0])
                s1_data_o.next = m2_data_i
                m2_data_o.next = s1_data_i

            elif m2_addr_i[31 + 1:28] == slave_2:
                s2_we_o.next = m2_we_i
                s2_addr_o.next = concat(modbv(0x0)[4:], m2_addr_i[27 + 1:0])
                s2_data_o.next = m2_data_i
                m2_data_o.next = s2_data_i

            elif m2_addr_i[31 + 1:28] == slave_3:
                s3_we_o.next = m2_we_i
                s3_addr_o.next = concat(modbv(0x0)[4:], m2_addr_i[27 + 1:0])
                s3_data_o.next = m2_data_i
                m2_data_o.next = s3_data_i

            elif m2_addr_i[31 + 1:28] == slave_4:
                s4_we_o.next = m2_we_i
                s4_addr_o.next = concat(modbv(0x0)[4:], m2_addr_i[27 + 1:0])
                s4_data_o.next = m2_data_i
                m2_data_o.next = s4_data_i

            elif m2_addr_i[31 + 1:28] == slave_5:
                s5_we_o.next = m2_we_i
                s5_addr_o.next = concat(modbv(0x0)[4:], m2_addr_i[27 + 1:0])
                s5_data_o.next = m2_data_i
                m2_data_o.next = s5_data_i

            else:
                pass

        elif grant == grant3:
            if m3_addr_i[31 + 1:28] == slave_0:
                s0_we_o.next = m3_we_i
                s0_addr_o.next = concat(modbv(0x0)[4:], m3_addr_i[27 + 1:0])
                s0_data_o.next = m3_data_i
                m3_data_o.next = s0_data_i

            elif m3_addr_i[31 + 1:28] == slave_1:
                s1_we_o.next = m3_we_i
                s1_addr_o.next = concat(modbv(0x0)[4:], m3_addr_i[27 + 1:0])
                s1_data_o.next = m3_data_i
                m3_data_o.next = s1_data_i

            elif m3_addr_i[31 + 1:28] == slave_2:
                s2_we_o.next = m3_we_i
                s2_addr_o.next = concat(modbv(0x0)[4:], m3_addr_i[27 + 1:0])
                s2_data_o.next = m3_data_i
                m3_data_o.next = s2_data_i

            elif m3_addr_i[31 + 1:28] == slave_3:
                s3_we_o.next = m3_we_i
                s3_addr_o.next = concat(modbv(0x0)[4:], m3_addr_i[27 + 1:0])
                s3_data_o.next = m3_data_i
                m3_data_o.next = s3_data_i

            elif m3_addr_i[31 + 1:28] == slave_4:
                s4_we_o.next = m3_we_i
                s4_addr_o.next = concat(modbv(0x0)[4:], m3_addr_i[27 + 1:0])
                s4_data_o.next = m3_data_i
                m3_data_o.next = s4_data_i

            elif m3_addr_i[31 + 1:28] == slave_5:
                s5_we_o.next = m3_we_i
                s5_addr_o.next = concat(modbv(0x0)[4:], m3_addr_i[27 + 1:0])
                s5_data_o.next = m3_data_i
                m3_data_o.next = s5_data_i

            else:
                pass

        else:
            pass


    return instances()
