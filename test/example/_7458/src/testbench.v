`timescale 1ns / 1ps

module testbench;

    // DUT 的接口信号
    reg [6:0] p1; // 假设 p1 有 6 个输入信号
    reg [4:0] p2; // 假设 p2 有 4 个输入信号
    wire p1y;    // p1 的输出信号
    wire p2y;    // p2 的输出信号

    // 实例化 DUT
    _7458 uut (
        .p1a(p1[0]), .p1b(p1[1]), .p1c(p1[2]), .p1d(p1[3]),
        .p1e(p1[4]), .p1f(p1[5]), .p1y(p1y),
        .p2a(p2[0]), .p2b(p2[1]), .p2c(p2[2]), .p2d(p2[3]),
        .p2y(p2y)
    );

    // 测试所有可能的输入组合
    initial begin
        $timeformat(-8, 3, " ns", 10);
        #0;
        for (p1 = 0; p1 < 4; p1 = p1 + 1) begin
            for (p2 = 0; p2 < 4; p2 = p2 + 1) begin
                #10; // 等待一段时间以观察输出
                $display("time: %5t, p1: %b p2: %b | p1y: %b p2y: %b", $time ,p1, p2, p1y, p2y);
            end
        end
        #20;
        $finish;
    end

endmodule
