// `timescale 1ns / 1ps

module ram_tb;

    // Inputs
    reg clk;
    reg rst;
    reg we_i;
    reg [31:0] addr_i;
    reg [31:0] data_i;

    // Outputs
    wire [31:0] data_o;

    // 实例化RAM模块
    ram uut (
        .clk(clk),
        .rst(rst),
        .we_i(we_i),
        .addr_i(addr_i),
        .data_i(data_i),
        .data_o(data_o)
    );

    // 时钟生成
    always #10 clk = ~clk; // 产生50MHz的时钟信号

    // 初始化输入并应用测试
    initial begin
        // 初始化输入
        clk = 0;
        rst = 1;
        we_i = 0;
        addr_i = 0;
        data_i = 0;

        // 等待时钟稳定
        #100;

        // 重置模块
        rst = 0;
        #100;
        rst = 1;

        // 测试写入和读取操作
        // 写入数据到地址0
        we_i = 1;
        addr_i = 32'h0000_0000;
        data_i = 32'hAAAA_AAAA;
        #20; // 等待一个时钟周期以完成写入

        // 读取地址0的数据
        we_i = 0;
        addr_i = 32'h0000_0000;
        #20; // 等待一个时钟周期以完成读取

        // 检查输出数据是否正确
        if (data_o === 32'hAAAA_AAAA) begin
            $display("Test passed: Data read matches data written.");
        end else begin
            $display("Test failed: Data %x read does not match data written.", data_o);
        end

        // 结束仿真
        #100;

        we_i = 1;
        addr_i = 32'h0000_0000;
        data_i = 32'hAAAA_ACDA;
        #20; // 等待一个时钟周期以完成写入

        // 读取地址0的数据
        we_i = 0;
        addr_i = 32'h0000_0000;
        #20; // 等待一个时钟周期以完成读取

        // 检查输出数据是否正确
        if (data_o === 32'hAAAA_ACDA) begin
            $display("Test passed: Data read matches data written.");
        end else begin
            $display("Test failed: Data %x read does not match data written.", data_o);
        end
        $finish;
    end

endmodule
