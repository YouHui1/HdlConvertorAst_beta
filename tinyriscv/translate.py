from hdlConvertor import HdlConvertor
import sys
import os
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# print(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from hdlConvertorAst.language import Language

from hdlConvertorAst.to.myhdl.myhdl import ToMyhdl
from hdlConvertorAst.to.json import ToJson

import json

input_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'rtl')
# print(os.path.exists(tinyriscv_path))
target_path = 'translate'

folder = ['utils', 'soc', 'core', 'perips']

for i in folder:
    if not os.path.exists(os.path.join(target_path, i)):
        os.mkdir(os.path.join(target_path, i))

def generate(DEBUG=False):
    for i in range(4):
        soc_input = os.path.join(input_path, folder[i])
        soc_output = os.path.join(target_path, folder[i])


        verilog_files = os.listdir(soc_input)

        for v in verilog_files:
            print(v)
            name = v.split('.')[0]
            lang = Language.VERILOG_2005
            c = HdlConvertor()

            res = c.parse(os.path.join(soc_input, v), lang, [])
            if DEBUG:
                with open(os.path.join(soc_output, name+'.json'), 'w') as f:
                    jv = ToJson()
                    j = jv.visit_HdlContext(res)
                    json.dump(j, f, indent=4, separators=(',',":"))

            # myhdl
            with open(os.path.join(soc_output, name+'.py'), 'w') as f:
                # tv = ToVerilog2005(sys.stdout)
                tv = ToMyhdl(f)
                tv.visit_HdlContext(res)

generate(True)
