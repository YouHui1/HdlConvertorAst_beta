module FSM_tb;

reg clk;
reg reset;
wire state_out;

// 实例化DUT
FSM uut (
    .clk(clk),
    .reset(reset),
    .state_out(state_out)
);

// 生成时钟信号
initial begin
    clk = 0;
    forever #10 clk = ~clk; // 假设时钟周期为20ns
end

// 测试序列
initial begin
    // 初始化输入
    reset = 1;
    #40; // 等待两个时钟周期以应用复位

    reset = 0; // 释放复位
    #1000; // 等待一段时间观察状态机行为

    // 结束仿真
    $finish;
end

// 监视变量变化
initial begin
    $monitor("Time = %0t, reset = %b, state_out = %b", $time, reset, state_out);
end

endmodule
