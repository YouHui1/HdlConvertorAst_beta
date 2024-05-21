// Testbench for the Shift Operations Module
module shift_tb;

    reg  [7:0] in_vector;
    wire [7:0] out_lsh;
    wire [7:0] out_rsh;
    wire [7:0] out_ash;
    wire [7:0] out_rotl;
    wire [7:0] out_rotr;

    // Instantiate the DUT
    shift_dut uut (
        .in_vector(in_vector),
        .out_lsh(out_lsh),
        .out_rsh(out_rsh),
        .out_ash(out_ash),
        .out_rotl(out_rotl),
        .out_rotr(out_rotr)
    );

    // Test the DUT
    initial begin
        // Initialize input vector
        in_vector = 8'b11101011;

        // Wait for the simulation to process the change
        #10;

        // Display results
        $display("in_vector: %b", in_vector);
        $display("out_lsh: %b (Logical shift left)", out_lsh);
        $display("out_rsh: %b (Logical shift right)", out_rsh);
        $display("out_ash: %b (Arithmetic shift right)", out_ash);
        $display("out_rotl: %b (Rotate left)", out_rotl);
        $display("out_rotr: %b (Rotate right)", out_rotr);

        // Change input vector and repeat
        in_vector = 8'b11111111;
        #10;
        // ... (Repeat display statements)
        $display("in_vector: %b", in_vector);
        $display("out_lsh: %b (Logical shift left)", out_lsh);
        $display("out_rsh: %b (Logical shift right)", out_rsh);
        $display("out_ash: %b (Arithmetic shift right)", out_ash);
        $display("out_rotl: %b (Rotate left)", out_rotl);
        $display("out_rotr: %b (Rotate right)", out_rotr);

        // End simulation
        $finish;
    end

endmodule
