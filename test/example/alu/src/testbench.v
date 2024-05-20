module ALU_tb;

    // Parameters
    parameter PERIOD = 10; // 时钟周期为10纳秒

    // Inputs
    reg clk;
    reg rst;
    reg [31:0] io_input1;
    reg [31:0] io_input2;
    reg [4:0] io_function;

    // Outputs
    wire [31:0] io_output;

    // 实例化ALU模块
    ALU uut (
        .clk(clk),
        .rst(rst),
        .io_input1(io_input1),
        .io_input2(io_input2),
        .io_function(io_function),
        .io_output(io_output)
    );

    // 生成时钟信号
    initial begin
        clk = 0;
        forever #(PERIOD/2) clk = ~clk;
    end

    // 测试序列
    initial begin
        // 初始化输入
        rst = 1;
        io_input1 = 32'h1242512f;
        io_input2 = 32'hfa34512f;
        io_function = 0;
        $display("Time = %0t, rst = %b, io_input1 = %h, io_input2 = %h, io_function = %b, io_output = %h",
                 $time, rst, io_input1, io_input2, io_function, io_output);
        #(PERIOD*10); // 等待两个时钟周期以应用复位

        // 释放复位
        rst = 0;
        $display("Time = %0t, rst = %b, io_input1 = %h, io_input2 = %h, io_function = %b, io_output = %h",
                 $time, rst, io_input1, io_input2, io_function, io_output);
        #(PERIOD*10);

        // 测试加法
        io_input1 = 32'h12345678;
        io_input2 = 32'h9abcdef;
        io_function = 8'h0;
        $display("Time = %0t, rst = %b, io_input1 = %h, io_input2 = %h, io_function = %b, io_output = %h",
                 $time, rst, io_input1, io_input2, io_function, io_output);
        #(PERIOD*10); // 等待10个时钟周期

        // 测试逻辑左移
        io_input1 = 32'h12345678;
        io_input2 = 32'h00000004;
        io_function = 8'h1;
        $display("Time = %0t, rst = %b, io_input1 = %h, io_input2 = %h, io_function = %b, io_output = %h",
                 $time, rst, io_input1, io_input2, io_function, io_output);
        #(PERIOD*10);

        // 测试异或
        io_input1 = 32'h12345678;
        io_input2 = 32'h9abcdef0;
        io_function = 8'h2;
        $display("Time = %0t, rst = %b, io_input1 = %h, io_input2 = %h, io_function = %b, io_output = %h",
                 $time, rst, io_input1, io_input2, io_function, io_output);
        #(PERIOD*10);

        // 测试逻辑右移
        io_input1 = 32'h12345678;
        io_input2 = 32'h00000004;
        io_function = 8'h3;
        $display("Time = %0t, rst = %b, io_input1 = %h, io_input2 = %h, io_function = %b, io_output = %h",
                 $time, rst, io_input1, io_input2, io_function, io_output);
        #(PERIOD*10);

        // 测试或
        io_input1 = 32'h12345678;
        io_input2 = 32'h9abcdef0;
        io_function = 8'h4;
        $display("Time = %0t, rst = %b, io_input1 = %h, io_input2 = %h, io_function = %b, io_output = %h",
                 $time, rst, io_input1, io_input2, io_function, io_output);
        #(PERIOD*10);

        // 测试与
        io_input1 = 32'h12345678;
        io_input2 = 32'h9abcdef0;
        io_function = 8'h5;
        $display("Time = %0t, rst = %b, io_input1 = %h, io_input2 = %h, io_function = %b, io_output = %h",
                 $time, rst, io_input1, io_input2, io_function, io_output);
        #(PERIOD*10);

        // 测试减法
        io_input1 = 32'h12345678;
        io_input2 = 32'h9abcdef0;
        io_function = 8'h6;
        $display("Time = %0t, rst = %b, io_input1 = %h, io_input2 = %h, io_function = %b, io_output = %h",
                 $time, rst, io_input1, io_input2, io_function, io_output);
        #(PERIOD*10);

        // 测试算术右移
        io_input1 = 32'h12345678;
        io_input2 = 32'h00000004;
        io_function = 8'h7;
        $display("Time = %0t, rst = %b, io_input1 = %h, io_input2 = %h, io_function = %b, io_output = %h",
                 $time, rst, io_input1, io_input2, io_function, io_output);
        #(PERIOD*10);

        // 测试比较（有符号）
        io_input1 = 32'h80000000;
        io_input2 = 32'h7fffffff;
        io_function = 8'h8;
        $display("Time = %0t, rst = %b, io_input1 = %h, io_input2 = %h, io_function = %b, io_output = %h",
                 $time, rst, io_input1, io_input2, io_function, io_output);
        #(PERIOD*10);

        // 测试比较（无符号）
        io_input1 = 32'h80000000;
        io_input2 = 32'h7fffffff;
        io_function = 8'h9;
        $display("Time = %0t, rst = %b, io_input1 = %h, io_input2 = %h, io_function = %b, io_output = %h",
                 $time, rst, io_input1, io_input2, io_function, io_output);
        #(PERIOD*10);

        // 结束模拟
        $finish;
    end


endmodule
