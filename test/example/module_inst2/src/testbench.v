// Testbench模块定义
module my_dut_tb;

// 测试信号定义
reg [15:0] tb_data_in;
wire [3:0] tb_data_out;

// 实例化DUT模块
my_dut uut (
    .data_in(tb_data_in),
    .data_out(tb_data_out)
);

initial begin
    // 初始化输入信号
    tb_data_in = 16'b0000000010101010;

    // 检查输出是否正确
    #10;  // 等待10个时间单位
    if(tb_data_out === 4'b1010) begin
        $display("Test passed: data_out is correctly selected.");
    end else begin
        $display("Test failed: data_out is not correctly selected.");
    end

    // 更改输入信号并再次检查
    tb_data_in = 16'b0000000011110000;
    #10;
    if(tb_data_out === 4'b1111) begin
        $display("Test passed: data_out is correctly selected after update.");
    end else begin
        $display("Test failed: data_out is not correctly selected after update.");
    end

    // 结束仿真
    $finish;
end

endmodule
