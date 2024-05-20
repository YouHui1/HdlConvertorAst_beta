module dut (
    input wire[7:0] data_in,
    // 8-bit input vector
    output reg[3:0] slice_plus,
    // Output for addition slice
    output reg[3:0] slice_minus
);
    // Perform addition slice from bit 4 with a width of 4
    always @(data_in)
        slice_plus = data_in[4 +: 4];
    // Perform subtraction slice from bit 4 with a width of 4
    always @(data_in)
        slice_minus = data_in[4 -: 4];
endmodule
