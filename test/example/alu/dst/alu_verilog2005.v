module ALU (
    input wire clk,
    input wire rst,
    input wire[31:0] io_input1,
    input wire[31:0] io_input2,
    input wire[4:0] io_function,
    output reg[31:0] io_output
);
    always @(io_input1, io_input2, io_function) begin: ALU_RTL
        case(io_function)
            0:
                io_output = io_input1 + io_input2;
            1:
                io_output = io_input1 << io_input2[5 - 1:0];
            2:
                io_output = io_input1 ^ io_input2;
            3:
                io_output = io_input1 >>> io_input2[5 - 1:0];
            4:
                io_output = io_input1 | io_input2;
            5:
                io_output = io_input1 & io_input2;
            6:
                io_output = io_input1 - io_input2;
            7:
                io_output = $signed($signed(io_input1) >>> io_input2[5 - 1:0]);
            8:
                io_output = {31'h0, $signed(io_input1) < $signed(io_input2)};
            9:
                io_output = {31'h0, io_input1 < io_input2};
            default:
                io_output = 0;
        endcase
    end

endmodule
