module dut (
    input wire clk,
    input wire[7:0] a,
    input wire[7:0] b,
    output reg[15:0] out1,
    output reg[15:0] out2,
    output reg[15:0] out3,
    output reg[15:0] out4,
    output reg[7:0] out5,
    output reg[7:0] out6
);
    reg[7:0] arr[3:0];
    // 4x8位的数组
    reg[15:0] vec;
    // 16位的向量
    always @(*) begin
        arr[0] = a;
        arr[1] = b;
        arr[2] = a + b;
        arr[3] = a - b;
        vec = {arr[0], arr[1]};
        out1 = {{7'b0, 1'b1}, arr[2]};
        out2 = {4{a[3:0]}};
        out3 = {b, a};
        out4 = {vec[15:8], vec[7:0]};
    end

    always @(posedge clk)
        {out5, out6} <= {a, b};
endmodule
