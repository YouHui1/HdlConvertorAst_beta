from reduction_myhdl import *

@block
def testbench():
    in_vector = Signal(modbv(0)[8:])
    out_and = Signal(modbv(0)[1:])
    out_or = Signal(modbv(0)[1:])
    out_nand = Signal(modbv(0)[1:])
    out_nor = Signal(modbv(0)[1:])
    out_xor = Signal(modbv(0)[1:])
    out_nxor = Signal(modbv(0)[1:])

    uut = reduction_dut(
        in_vector=in_vector,
        out_and=out_and,
        out_or=out_or,
        out_nand=out_nand,
        out_nor=out_nor,
        out_xor=out_xor,
        out_nxor=out_nxor
    )

    @instance
    def test():
        in_vector.next = 0
        yield delay(10)
        print(f"in_vector: {in_vector}, out_and: {out_and}, out_or: {out_or}, out_nor: {out_nor}, out_nand: {out_nand}, out_nor: {out_nor}, out_xor: {out_xor}, out_nxor: {out_nxor}")

        in_vector.next = 0b10101010
        yield delay(10)
        print(f"in_vector: {in_vector}, out_and: {out_and}, out_or: {out_or}, out_nor: {out_nor}, out_nand: {out_nand}, out_nor: {out_nor}, out_xor: {out_xor}, out_nxor: {out_nxor}")

        in_vector.next = 0b10111011
        yield delay(10)
        print(f"in_vector: {in_vector}, out_and: {out_and}, out_or: {out_or}, out_nor: {out_nor}, out_nand: {out_nand}, out_nor: {out_nor}, out_xor: {out_xor}, out_nxor: {out_nxor}")

        in_vector.next = 0b00110011
        yield delay(10)
        print(f"in_vector: {in_vector}, out_and: {out_and}, out_or: {out_or}, out_nor: {out_nor}, out_nand: {out_nand}, out_nor: {out_nor}, out_xor: {out_xor}, out_nxor: {out_nxor}")

        in_vector.next = 0b00110010
        yield delay(10)
        print(f"in_vector: {in_vector}, out_and: {out_and}, out_or: {out_or}, out_nor: {out_nor}, out_nand: {out_nand}, out_nor: {out_nor}, out_xor: {out_xor}, out_nxor: {out_nxor}")

        in_vector.next = 0b11111111
        yield delay(10)
        print(f"in_vector: {in_vector}, out_and: {out_and}, out_or: {out_or}, out_nor: {out_nor}, out_nand: {out_nand}, out_nor: {out_nor}, out_xor: {out_xor}, out_nxor: {out_nxor}")

        raise StopSimulation

    return instances()

tb = testbench()
tb.run_sim()
