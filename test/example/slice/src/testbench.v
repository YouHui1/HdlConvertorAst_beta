module tb_dut();
    reg [7:0] data_in;
    wire [3:0] slice_plus;
    wire [3:0] slice_minus;

    dut uut (
        .data_in(data_in),
        .slice_plus(slice_plus),
        .slice_minus(slice_minus)
    );

    initial begin
        #10;
        // Test various input values
        data_in = 8'b11010101; // Test case 1
        #10; // Wait for the output to settle

        data_in = 8'b10101010; // Test case 2
        #10;

        data_in = 8'b11110000; // Test case 3
        #10;

        // Add more test cases if necessary

        $finish;
    end

    // Display output for each test case
    initial begin
        #0;
        forever begin
            #10 $display("data_in = %b, slice_plus = %b, slice_minus = %b", data_in, slice_plus, slice_minus);
        end
    end
endmodule
