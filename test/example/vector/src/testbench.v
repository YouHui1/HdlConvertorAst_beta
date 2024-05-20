`timescale 1ns/1ps

module dut_tb;

    reg clk;
    reg [7:0] a;
    reg [7:0] b;
    wire [15:0] out1;
    wire [15:0] out2;
    wire [15:0] out3;
    wire [15:0] out4;
    wire [7:0] out5;
    wire [7:0] out6;

    dut dut_inst (
        .clk(clk),
        .a(a),
        .b(b),
        .out1(out1),
        .out2(out2),
        .out3(out3),
        .out4(out4),
        .out5(out5),
        .out6(out6)
    );

    initial begin
        clk = 0;
        a = 8'h12;
        b = 8'h34;

        #10
        a = 8'h56;
        b = 8'h78;

        #10
        a = 8'hab;
        b = 8'hcd;

        #10
        a = 8'hef;
        b = 8'h01;

        #10
        a = 8'h80;
        b = 8'h80;

        #10
        a = 8'hff;
        b = 8'hff;

        #10
        a = 8'h00;
        b = 8'h00;

        #10
        a = 8'h01;
        b = 8'h02;

        #10
        a = 8'h03;
        b = 8'h04;

        #10
        a = 8'h05;
        b = 8'h06;

        #10
        a = 8'h07;
        b = 8'h08;

        #10
        a = 8'h09;
        b = 8'h0a;

        #10
        a = 8'h0b;
        b = 8'h0c;

        #10
        a = 8'h0d;
        b = 8'h0e;

        #10
        a = 8'h0f;
        b = 8'h10;

        #20 $finish;
    end

    always #5 clk = ~clk;

    always @(posedge clk) begin
        $display("a = %h, b = %h, out1 = %h, out2 = %h, out3 = %h, out4 = %h, out5 = %h, out6 = %h",
                    a, b, out1, out2, out3, out4, out5, out6);
    end

endmodule
