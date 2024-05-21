from shift_myhdl import *

@block
def testbench():
    in_vector = Signal(modbv(0)[8:])
    out_lsh = Signal(modbv(0)[8:])
    out_rsh = Signal(modbv(0)[8:])
    out_ash = Signal(modbv(0)[8:])
    out_rotl = Signal(modbv(0)[8:])
    out_rotr = Signal(modbv(0)[8:])


    uut = shift_dut(
        in_vector=in_vector,
        out_lsh=out_lsh,
        out_rsh=out_rsh,
        out_ash=out_ash,
        out_rotl=out_rotl,
        out_rotr=out_rotr
    )

    @instance
    def test():
        in_vector.next = 0b11101011
        yield delay(10)
        print(f"in_vector: {in_vector}");
        print(f"out_lsh: {out_lsh} (Logical shift left)");
        print(f"out_rsh: {out_rsh} (Logical shift right)");
        print(f"out_ash: {out_ash} (Arithmetic shift right)");
        print(f"out_rotl: {out_rotl} (Rotate left)");
        print(f"out_rotr: {out_rotr} (Rotate right)");

        in_vector.next = 0b11111111
        yield delay(10)
        print(f"in_vector: {in_vector}");
        print(f"out_lsh: {out_lsh} (Logical shift left)");
        print(f"out_rsh: {out_rsh} (Logical shift right)");
        print(f"out_ash: {out_ash} (Arithmetic shift right)");
        print(f"out_rotl: {out_rotl} (Rotate left)");
        print(f"out_rotr: {out_rotr} (Rotate right)");

        raise StopSimulation

    return instances()

tb = testbench()
tb.run_sim()
