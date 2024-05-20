// DUT: Reduction Operations Module
module reduction_dut (
    input [7:0] in_vector,  // 8-bit input vector
    output out_and,        // AND reduction output
    output out_or,         // OR reduction output
    output out_nand,        // NAND reduction output
    output out_nor,        // NOR reduction output
    output out_xor,         // XOR reduction output
    output out_nxor         // NXOR reduction output
);

    // AND reduction: All bits must be 1 for the output to be 1
    assign out_and = &(in_vector);

    // OR reduction: At least one bit must be 1 for the output to be 1
    assign out_or = |in_vector;

    // NAND reduction: At least one bit must be 0 for the output to be 1
    assign out_nand = ~&(in_vector);

    // NOR reduction: All bits must be 0 for the output to be 1
    assign out_nor = ~|(in_vector);

    // XOR reduction: the counts of one bit must be odd for the output to be 1
    assign out_xor = ^(in_vector);

    // NXOR reduction: the counts of one bit must be even for the output to be 1
    assign out_nxor = ~^(in_vector);

endmodule
