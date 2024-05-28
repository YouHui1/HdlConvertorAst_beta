import sys
import os
# print(os.path.abspath(os.curdir))
sys.path.append(os.path.abspath(os.curdir))
from soc.tinyriscv_soc_top import *

@block
def tinyriscv_soc_tb(src_file):
    clk = Signal(True)
    rst = Signal(True)

    tinyriscv_soc_top_0 = tinyriscv_soc_top(
        clk=clk,
        rst=rst,
        uart_debug_pin=Signal(modbv(0)[1:]),
        succ=Signal(modbv(0)[1:]),
        over=Signal(modbv(0)[1:]),
        halted_ind=Signal(modbv(0)[1:]),
        uart_tx_pin=Signal(modbv(0)[1:]),
        # UART发送引脚
        uart_rx_pin=Signal(modbv(0)[1:]),
        # UART接收引脚
        gpio=Signal(modbv(0)[1:]),
        # GPIO引脚
        jtag_TCK=Signal(modbv(0)[1:]),
        # JTAG TCK引脚
        jtag_TMS=Signal(modbv(0)[1:]),
        # JTAG TMS引脚
        jtag_TDI=Signal(modbv(0)[1:]),
        # JTAG TDI引脚
        jtag_TDO=Signal(modbv(0)[1:]),
        # JTAG TDO引脚
        spi_miso=Signal(modbv(0)[1:]),
        # SPI MISO引脚
        spi_mosi=Signal(modbv(0)[1:]),
        # SPI MOSI引脚
        spi_ss=Signal(modbv(0)[1:]),
        # SPI SS引脚
        spi_clk=Signal(modbv(0)[1:])
    )

    @always(delay(10))
    def driver():
        clk.next = not clk

    @instance
    def test():
        # yield delay(0)
        x3 = u_regs[3]
        x26 = u_regs[26]
        x27 = u_regs[27]

        clk.next = 0
        rst.next = 0
        # yield delay(0)

        print("test running...")

        yield delay(40)
        rst.next = 1
        yield delay(200)
        if x26 == 0:
            yield x26
        yield delay(100)
        if x27 == 1:
            print(f"time: {now()}      ")
            print("~~~~~~~~~~~~~~~~~~~ TEST_PASS ~~~~~~~~~~~~~~~~~~~")
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            print("~~~~~~~~~ #####     ##     ####    #### ~~~~~~~~~")
            print("~~~~~~~~~ #    #   #  #   #       #     ~~~~~~~~~")
            print("~~~~~~~~~ #    #  #    #   ####    #### ~~~~~~~~~")
            print("~~~~~~~~~ #####   ######       #       #~~~~~~~~~")
            print("~~~~~~~~~ #       #    #  #    #  #    #~~~~~~~~~")
            print("~~~~~~~~~ #       #    #   ####    #### ~~~~~~~~~")
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        else:
            print(f"time: {now()}      ")
            print("~~~~~~~~~~~~~~~~~~~ TEST_FAIL ~~~~~~~~~~~~~~~~~~~~")
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            print("~~~~~~~~~~######    ##       #    #     ~~~~~~~~~~")
            print("~~~~~~~~~~#        #  #      #    #     ~~~~~~~~~~")
            print("~~~~~~~~~~#####   #    #     #    #     ~~~~~~~~~~")
            print("~~~~~~~~~~#       ######     #    #     ~~~~~~~~~~")
            print("~~~~~~~~~~#       #    #     #    #     ~~~~~~~~~~")
            print("~~~~~~~~~~#       #    #     #    ######~~~~~~~~~~")
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            print(f'fail testnum = {x3}')
            for r in range(32):
                print(f"x{r} = {hex(u_regs[r])}")

        raise StopSimulation

    @instance
    def timeout():
        # yield delay(500000)
        yield delay(20000)
        print("Time Out.")
        raise StopSimulation

    @instance
    def read_mem():
        # yield delay(0)
        with open(src_file, 'r') as f:
            data = f.readlines()
            for idx, i in enumerate(data):
                u_rom[idx].next = (int(i[:-1], 16))

        yield delay(0)
        # for i in range(355):
        #     print(i, u_rom[i])


    return instances()
    pass

def test(src, wave: bool=False, name=None):
    tb = tinyriscv_soc_tb(src)
    if wave:
        tb.config_sim(wave, name=name)
    tb.run_sim()
    return

def main():
    print(r'python test/BinToMem_CLI.py' + ' ' + sys.argv[1] + ' ' + sys.argv[2])
    cmd = r'python test/BinToMem_CLI.py' + ' ' + sys.argv[1] + ' ' + sys.argv[2]
    # if not os.path.exists(sys.argv[2]):
    f = os.popen(cmd)
    f.close()

    test(sys.argv[2])
    return


if __name__ == '__main__':
    sys.exit(main())
