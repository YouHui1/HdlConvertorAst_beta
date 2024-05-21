from hdlConvertor import HdlConvertor
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# print(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from hdlConvertorAst.language import Language

from hdlConvertorAst.to.verilog.verilog2005 import ToVerilog2005

from hdlConvertorAst.to.myhdl.myhdl import ToMyhdl
from hdlConvertorAst.to.json import ToJson

import json


input_path = 'test/example/'

def testone(path):
    folder = os.path.join(input_path, path)
    name = os.path.basename(folder)

    # 指定要解析的文件的语言（在这个例子中是 Verilog）
    lang = Language.VERILOG_2005
    # 创建一个 hdlConvertor 对象
    c = HdlConvertor()

    res = c.parse(f'{folder}/src/{name}.v', lang, [])



    # if not os.path.exists(f"{folder}/dst"):
    #     os.mkdir(f"{folder}/dst")

    with open(f'{folder}/dst/{name}.json', 'w') as f:
        jv = ToJson()
        j = jv.visit_HdlContext(res)
        json.dump(j, f, indent=4, separators=(',',":"))

    # verilog
    with open(f'{folder}/dst/{name}_verilog2005.v', 'w') as f:
        tv = ToVerilog2005(f)
        tv.visit_HdlContext(res)

    # myhdl
    with open(f'{folder}/dst/{name}_myhdl.py', 'w') as f:
        # tv = ToVerilog2005(sys.stdout)
        tv = ToMyhdl(f)
        tv.visit_HdlContext(res)

# testone('_7458')
# testone('normal')
# testone('module_inst')
testone('vector')
# testone('alu')

def testall():
    lst = os.listdir(input_path)
    for path in lst:
        folder = os.path.join(input_path, path)
        name = os.path.basename(folder)

        # 指定要解析的文件的语言（在这个例子中是 Verilog）
        lang = Language.VERILOG_2005
        # 创建一个 hdlConvertor 对象
        c = HdlConvertor()

        res = c.parse(f'{folder}/src/{name}.v', lang, [])

        # if not os.path.exists(f"{folder}/dst"):
        #     os.mkdir(f"{folder}/dst")

        with open(f'{folder}/dst/{name}.json', 'w') as f:
            jv = ToJson()
            j = jv.visit_HdlContext(res)
            json.dump(j, f, indent=4, separators=(',',":"))

        # verilog
        with open(f'{folder}/dst/{name}_verilog2005.v', 'w') as f:
            tv = ToVerilog2005(f)
            tv.visit_HdlContext(res)

        # myhdl
        with open(f'{folder}/dst/{name}_myhdl.py', 'w') as f:
            # tv = ToVerilog2005(sys.stdout)
            tv = ToMyhdl(f)
            tv.visit_HdlContext(res)


# testall()
