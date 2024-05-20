module FSM #(
    // 定义状态
    parameter S0 = 0,
    parameter S1 = 1,
    parameter S2 = 2
) (
    input wire clk,
    input wire reset,
    output reg state_out
);
    // 状态机当前状态
    reg[1:0] current_state;
    // 初始块，使用while循环进行状态初始化
    initial
        while (1) begin
            @(posedge clk)
            ;
            if (reset)
                current_state = S0;
            else
                case(current_state)
                    S0:
                        current_state = S1;
                    S1:
                        current_state = S2;
                    S2:
                        current_state = S0;
                    default:
                        current_state = S0;
                endcase
        end

    // 将当前状态输出到state_out
    always @(posedge clk)
        if (reset)
            state_out <= 1'b0;
        else
            state_out <= current_state[0];
endmodule
