from myhdl import *

@block
def calculate (
    data_in,
    # 8-bit 输入信号
    data_out
):

    # 假设我们选择data_in的高4位
    @always(data_in)
    def seq_0():
        data_out.next = data_in[7 + 1:4]
    return instances()
# DUT模块定义
@block
def my_dut (
    data_in,
    # 8-bit 输入信号
    data_out
):

    cal = calculate(
        data_in=data_in(7 + 1,0),
        data_out=data_out
    )
    return instances()
