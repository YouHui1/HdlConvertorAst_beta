// Testbench for the top_module
module top_tb;

    // Signals for the testbench
    reg clk;
    reg [1:0] data_in;
    wire [2:0] data_out;

    // Instantiate the DUT
    top_module uut (
        .clk(clk),
        .data_in(data_in),
        .data_out(data_out)
    );

    // Clock generation
    initial begin
        clk = 0;
        forever #5 clk = ~clk;
    end

    // Test the DUT
    initial begin
        #20 data_in = 2'b00;
        #20 data_in = 2'b01;
        #20 data_in = 2'b10;
        #20 data_in = 2'b11;
        #20 $finish;
    end

    // Display the results
    initial begin
        $monitor("Time = %0t, data_in = %b, data_out = %b", $time, data_in, data_out);
    end

endmodule
