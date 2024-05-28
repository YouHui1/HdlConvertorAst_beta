from testbench import test
import sys
import os

if __name__ == '__main__':
    test(sys.argv[1], True, 'test/vcd/'+os.path.basename(sys.argv[1]))
