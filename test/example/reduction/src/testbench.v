// Testbench for the Reduction Operations Module
module reduction_tb;

    reg [7:0] in_vector;
    wire out_and;
    wire out_or;
    wire out_nand;
    wire out_nor;
    wire out_xor;
    wire out_nxor;

    // Instantiate the DUT
    reduction_dut uut (
        .in_vector(in_vector),
        .out_and(out_and),
        .out_or(out_or),
        .out_nand(out_nand),
        .out_nor(out_nor),
        .out_xor(out_xor),
        .out_nxor(out_nxor)
    );

    // Test the DUT
    initial begin
        // Test all zeros
        in_vector = 8'b00000000;
        #10; // Wait for the simulation to process the change
        // Check the outputs
        $display("in_vector: %b, out_and: %b, out_or: %b, out_nor: %b, out_nand: %b, out_nor: %b, out_xor: %b, out_nxor: %b", in_vector, out_and, out_or, out_nor, out_nand, out_nor, out_xor, out_nxor);

        // Test with a mix of ones and zeros
        in_vector = 8'b10101010;
        #10;
        $display("in_vector: %b, out_and: %b, out_or: %b, out_nor: %b, out_nand: %b, out_nor: %b, out_xor: %b, out_nxor: %b", in_vector, out_and, out_or, out_nor, out_nand, out_nor, out_xor, out_nxor);

        in_vector = 8'b10111011;
        #10;
        $display("in_vector: %b, out_and: %b, out_or: %b, out_nor: %b, out_nand: %b, out_nor: %b, out_xor: %b, out_nxor: %b", in_vector, out_and, out_or, out_nor, out_nand, out_nor, out_xor, out_nxor);

        in_vector = 8'b00110011;
        #10;
        $display("in_vector: %b, out_and: %b, out_or: %b, out_nor: %b, out_nand: %b, out_nor: %b, out_xor: %b, out_nxor: %b", in_vector, out_and, out_or, out_nor, out_nand, out_nor, out_xor, out_nxor);

        in_vector = 8'b00110010;
        #10;
        $display("in_vector: %b, out_and: %b, out_or: %b, out_nor: %b, out_nand: %b, out_nor: %b, out_xor: %b, out_nxor: %b", in_vector, out_and, out_or, out_nor, out_nand, out_nor, out_xor, out_nxor);

        // Test all ones
        in_vector = 8'b11111111;
        #10;
        $display("in_vector: %b, out_and: %b, out_or: %b, out_nor: %b, out_nand: %b, out_nor: %b, out_xor: %b, out_nxor: %b", in_vector, out_and, out_or, out_nor, out_nand, out_nor, out_xor, out_nxor);

        // End simulation
        $finish;
    end

endmodule
