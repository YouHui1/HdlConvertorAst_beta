from myhdl import *

@block
def FSM (
    clk,
    reset,
    state_out,
    # 定义状态
    S0 = 0,
    S1 = 1,
    S2 = 2
):
    # 状态机当前状态
    current_state = Signal(modbv(0)[1 + 1 - 0:])

    # 初始块，使用while循环进行状态初始化
    @instance
    def instance_0():
        yield delay(0)

        while 1: 
            yield clk.posedge

            if reset:
                current_state.next = S0
            else:
                if current_state == S0:
                    current_state.next = S1
                elif current_state == S1:
                    current_state.next = S2
                elif current_state == S2:
                    current_state.next = S0
                else:
                    current_state.next = S0

    # 将当前状态输出到state_out
    @always(clk.posedge)
    def seq_0():
        if reset:
            state_out.next = 0b0
        else:
            state_out.next = current_state[0]
    return instances()
