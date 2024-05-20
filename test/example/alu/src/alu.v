module ALU (
    clk,
    rst,
    io_input1,
    io_input2,
    io_function,
    io_output
);

input clk;
input rst;
input [31:0] io_input1;
input [31:0] io_input2;
input [4:0] io_function;
output [31:0] io_output;
reg [31:0] io_output;

always @(io_input1, io_input2, io_function) begin: ALU_RTL
    case (io_function)
        'h0: begin
            io_output = (io_input1 + io_input2);
        end
        'h1: begin
            io_output = (io_input1 << io_input2[5-1:0]);
        end
        'h2: begin
            io_output = (io_input1 ^ io_input2);
        end
        'h3: begin
            io_output = (io_input1 >>> io_input2[5-1:0]);
        end
        'h4: begin
            io_output = (io_input1 | io_input2);
        end
        'h5: begin
            io_output = (io_input1 & io_input2);
        end
        'h6: begin
            io_output = (io_input1 - io_input2);
        end
        'h7: begin
            io_output = $signed($signed(io_input1) >>> io_input2[5-1:0]);
        end
        'h8: begin
            io_output = {31'h0, ($signed(io_input1) < $signed(io_input2))};
        end
        'h9: begin
            io_output = {31'h0, (io_input1 < io_input2)};
        end
        default: begin
            io_output = 0;
        end
    endcase
end

endmodule
