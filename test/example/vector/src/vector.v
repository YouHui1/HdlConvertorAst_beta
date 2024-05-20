module dut (
    input clk,
    input [7:0] a,
    input [7:0] b,
    output reg [15:0] out1,
    output reg [15:0] out2,
    output reg [15:0] out3,
    output reg [15:0] out4,
    output reg [7:0] out5,
    output reg [7:0] out6

);
    reg [7:0] arr[3:0]; // 4x8位的数组
    reg [15:0] vec; // 16位的向量

    always @(*) begin
        // 数组赋值
        // parameter i = 0;
        // for (i = 0; i < 4; ++i) begin
        //   arr[0] = 8'B0;
        // end

        arr[0][1:0] = a;
        arr[1] = b;
        arr[2] = a + b;
        arr[3] = a - b;

        // 向量赋值
        vec = {arr[0], arr[1]}; // 连接两个8位数组元素形成16位向量

        // 不同的拼接表达式
        out1 = {7'b0, 1'b1, arr[2]}; // 8位高位补0,拼接8位数组元素
        out2 = {4{a[3:0]}}; // 复制a的低4位4次形成16位输出
        out3 = {b, a}; // 连接两个8位输入形成16位输出
        out4 = {vec[15:8], vec[7:0]}; // 左值拼接,交换16位向量的高低8位
    end
    always @(posedge clk) begin
        {out5, out6} <= {a, b};
    end
endmodule
