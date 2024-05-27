module ram (
    input wire clk,
    input wire rst,
    input wire we_i,
    // write enable
    input wire[31:0] addr_i,
    // addr
    input wire[31:0] data_i,
    output reg[31:0] data_o
);
    reg[31:0] _ram[0:4096 - 1];
    always @(posedge clk)
        if (we_i == 1'b1)
            _ram[addr_i[31:2]] <= data_i;
    always @(*)
        if (rst == 1'b0)
            data_o = 0;
        else
            data_o = _ram[addr_i[31:2]];
endmodule
