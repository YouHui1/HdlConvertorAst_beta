# Makefile

# 定义源代码文件夹
SRC_DIR = src

# 定义二进制文件夹
BIN_DIR = bin

# 定义源文件，包括 dut 和 testbench 文件
DUT_FILE = $(SRC_DIR)/vector.v
TB_FILE = $(SRC_DIR)/testbench.v

# 定义仿真的顶层模块（这里假设顶层模块是 testbench）
TOP_MODULE = testbench

# 定义生成的仿真输出文件的名称
SIM_OUTPUT = $(BIN_DIR)/testbench.vvp

# 定义仿真的可执行文件
SIM_EXECUTABLE = $(BIN_DIR)/testbench

# 定义 iverilog 的编译选项
IVERILOG_FLAGS = -o $(SIM_OUTPUT)

# 默认目标（运行仿真）
all: simulate

# 编译仿真文件
$(SIM_OUTPUT): $(DUT_FILE) $(TB_FILE)
	iverilog $(IVERILOG_FLAGS) $(DUT_FILE) $(TB_FILE)

# 运行仿真
simulate: $(SIM_OUTPUT)
	vvp $(SIM_OUTPUT)

# 清理生成的仿真文件
clean:
	rm -f $(SIM_OUTPUT)

.PHONY: all simulate clean
