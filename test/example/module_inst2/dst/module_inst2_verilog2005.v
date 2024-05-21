module calculate (
    input wire[7:0] data_in,
    // 8-bit 输入信号
    output reg[3:0] data_out
);
    // 假设我们选择data_in的高4位
    always @(data_in)
        data_out = data_in[7:4];
endmodule
// DUT模块定义
module my_dut (
    input wire[15:0] data_in,
    // 8-bit 输入信号
    output wire[3:0] data_out
);
    calculate cal (
        .data_in(data_in[7:0]),
        .data_out(data_out)
    );

endmodule
