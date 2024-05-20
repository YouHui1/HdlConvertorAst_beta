// DUT: Reduction and Shift Operations Module
module shift_dut (
    input signed [7:0] in_vector,  // 8-bit input vector
    output wire [7:0] out_lsh,      // Logical shift left output
    output wire [7:0] out_rsh,      // Logical shift right output
    output wire [7:0] out_ash,      // Arithmetic shift right output
    output wire [7:0] out_rotl,     // Rotate left output
    output wire [7:0] out_rotr      // Rotate right output
);

    // Logical shift left by 1 bit
    assign out_lsh = in_vector << 1;

    // Logical shift right by 1 bit
    assign out_rsh = in_vector >> 1;

    // Arithmetic shift right by 1 bit (same as logical shift for positive numbers)
    assign out_ash = in_vector >>> 1;

    // Rotate left by 1 bit
    assign out_rotl = {in_vector[0], in_vector[7:1]};

    // Rotate right by 1 bit
    assign out_rotr = {in_vector[6:0], in_vector[7]};

endmodule
