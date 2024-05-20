// 模块 A：一个简单的反相器
module inverter(
    input a,
    output b
);
    assign b = ~a;
endmodule

// 模块 B：一个简单的二输入与门
module and_gate(
    input a,
    input b,
    output c
);
    assign c = a & b;
endmodule

// 模块 C：一个简单的二输入或门
module or_gate(
    input a,
    input b,
    output c
);
    wire d;
    assign d = a | b;
    assign c = d;
endmodule

// DUT: Top-level module that instantiates modules A, B, and C
module top_module(
    input wire clk,
    input wire [1:0] data_in,
    output wire [2:0] data_out
);

    // Signals for module instances
    wire not_data;
    wire and_data;
    wire or_data;

    // Instance of module A
    inverter uut_inverter (
        .a(data_in[0]),
        .b(not_data)
    );

    // Instance of module B
    and_gate uut_and_gate (
        .a(data_in[0]),
        .b(data_in[1]),
        .c(and_data)
    );

    // Instance of module C
    or_gate uut_or_gate (
        .a(data_in[0]),
        .b(data_in[1]),
        .c(or_data)
    );

    // Connect the outputs
    assign data_out[0] = not_data;
    assign data_out[1] = and_data;
    assign data_out[2] = or_data;

endmodule
