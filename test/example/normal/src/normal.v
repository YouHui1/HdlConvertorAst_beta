module FSM (
    input wire clk,
    input wire reset,
    output reg state_out
);

// 定义状态
parameter S0 = 0, S1 = 1, S2 = 2;

// 状态机当前状态
reg [1:0] current_state;

// 初始块，使用while循环进行状态初始化
initial begin
    while (1) begin
        @(posedge clk);
        if (reset) begin
            current_state = S0;
        end else begin
            case (current_state)
                S0: current_state = S1;
                S1: current_state = S2;
                S2: current_state = S0;
                default: current_state = S0;
            endcase
        end
    end
end

// 将当前状态输出到state_out
always @(posedge clk) begin
    if (reset) begin
        state_out <= 1'b0;
    end else begin
        state_out <= current_state[0]; // 只输出当前状态的最低位
    end
end

endmodule
