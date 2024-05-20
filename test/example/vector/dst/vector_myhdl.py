from myhdl import *

@block
def dut (
    clk,
    a,
    b,
    out1,
    out2,
    out3,
    out4,
    out5,
    out6
):
    arr = Signal(modbv(0)[8:])
    # 4x8位的数组
    vec = Signal(modbv(0)[16:])

    # 16位的向量
    @always_comb
    def comb_0(): 
        arr[0].next[1 + 1:0] = a
        arr[1].next = b
        arr[2].next = a + b
        arr[3].next = a - b
        vec.next = concat(arr[0], arr[1])
        out1.next = concat(concat(modbv(0b0)[7:], modbv(0b1)[1:]), arr[2])
        out2.next = concat(concat(a[3 + 1:0]),concat(a[3 + 1:0]),concat(a[3 + 1:0]),concat(a[3 + 1:0]))
        out3.next = concat(b, a)
        out4.next = concat(vec[15 + 1:8], vec[7 + 1:0])

    @always(clk.posedge)
    def seq_0():
        tmp = concat(a, b)
        out6.next = tmp[8+0:0]
        out5.next = tmp[8+8+0:8+0]

    return instances()
