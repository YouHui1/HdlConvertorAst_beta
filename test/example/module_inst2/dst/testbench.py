from module_inst2_myhdl import *

@block
def my_dut_tb():
    tb_data_in = Signal(modbv(0)[16:])
    tb_data_out = Signal(modbv(0)[4:])

    uut = my_dut (
        data_in=tb_data_in,
        data_out=tb_data_out
    )

    @instance
    def driver():
        yield delay(0)
        tb_data_in.next = 0b0000000010101010
        yield delay(10)
        if tb_data_out == 0b1010:
            print('passed')
        else:
            print(f'failed: {tb_data_out}')

        tb_data_in.next = 0b0000000011110000
        yield delay(10)
        if tb_data_out == 0b1111:
            print('passed')
        else:
            print(f'failed: {tb_data_out}')

    return instances()

tb = my_dut_tb()
tb.run_sim()
