module calculate (
    input wire [7:0] data_in,  // 8-bit 输入信号
    output reg [3:0] data_out  // 4-bit 输出信号，是输入信号的片选
);

// 假设我们选择data_in的高4位
always @ (data_in) begin
    data_out = data_in[7:4];  // 选择data_in的高4位作为输出
end

endmodule

// DUT模块定义
module my_dut (
    input wire [15:0] data_in,  // 8-bit 输入信号
    output wire [3:0] data_out  // 4-bit 输出信号，是输入信号的片选
);
calculate cal (
    .data_in(data_in[7:0]),
    .data_out(data_out)
);

endmodule
