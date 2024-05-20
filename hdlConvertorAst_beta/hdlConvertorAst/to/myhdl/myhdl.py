from hdlConvertorAst.hdlAst import HdlDirection, HdlOpType, \
    HdlOp, HdlCompInst, HdlIdDef, iHdlStatement, \
    HdlTypeAuto, HdlFunctionDef
from hdlConvertorAst.to.hdlUtils import Indent, iter_with_last
from hdlConvertorAst.to.myhdl.stm import ToMyhdlStm
from hdlConvertorAst.to.myhdl.utils import collect_array_dims, get_wire_t_params
from hdlConvertorAst.to.myhdl.utils import save_port_dims, set_cur_module, search_from_dict
from hdlConvertorAst.to.myhdl.utils import extract_numbers

import io

class ToMyhdl(ToMyhdlStm):
    DIR2V = {
        HdlDirection.IN: "input",
        HdlDirection.OUT: "output",
        HdlDirection.INOUT: "inout",
    }

    def __init__(self, out_stream):
        ToMyhdlStm.__init__(self, out_stream)
        self._type_requires_nettype = True

        self.module = False

    def visit_doc(self, obj):
        return super(ToMyhdl, self).visit_doc(obj, "#")

    def visit_direction(self, d):
        """
        :type d: HdlDirection
        """
        vd = self.DIR2V[d]
        self.out.write(vd)

    def visit_generic_declr(self, g):
        """
        :type g: HdlIdDef
        """
        self.visit_doc(g)
        trnt = self._type_requires_nettype
        try:
            # self._type_requires_nettype = False
            w = self.out.write
            # if g.type is HdlTypeAuto:
            #     is_array = False
            # else:
            #     is_array = self.visit_type_first_part(g.type)
            #     w(" ")
            w(g.name)
            # if is_array:
            #     self.visit_type_array_part(g.type)
            v = g.value
            if v is not None:
                w(" = ")
                self.visit_iHdlExpr(v)
        finally:
            self._type_requires_nettype = trnt

    def visit_port_declr(self, p):
        """
        :type p: HdlIdDef
        """
        w = self.out.write
        self.visit_doc(p)
        # self.visit_direction(p.direction)
        # w(" ")

        t = p.type
        # if t is HdlTypeAuto:
        #     # w("wire ")
        #     is_array = False
        # else:
        #     is_array = self.visit_type_first_part(t)
        #     w(" ")

        w(p.name)
        t, array_dims = collect_array_dims(t)
        base_t, width, is_signed, _ = get_wire_t_params(t)

        f = io.StringIO()
        reg = self.out
        self.out = f

        if width is not None:
            self.visit_iHdlExpr(width)
            width = f.getvalue()
            nums = extract_numbers(width)
            sub = str(abs(int(nums[0]) - int(nums[1])) + 1)
            width = sub
        else:
            width = 1
        f.truncate(0)
        if array_dims is not None:
            array_dims = len(array_dims)

        save_port_dims(p.name, width, array_dims)

        self.out = reg
        # if is_array:
        #     self.visit_type_array_part(t)

    def visit_HdlIdDef(self, var):
        """
        :type var: HdlIdDef
        """
        self.visit_doc(var)
        name = var.name
        t = var.type

        w = self.out.write
        w(name)
        w(" = ")

        reg = self.out
        self.out = io.StringIO()
        f = self.out
        w = self.out.write


        if var.is_const:
            w("modbv(")
            assert var.value is not None, var.name
        else:
            w("Signal(modbv(")

        # w(f.getvalue())

        if var.value is not None:
            self.visit_iHdlExpr(var.value)
        else:
            w('0')
        w(')')

        width = 1
        array_dims = []
        if t is HdlTypeAuto:
            w('[1:]')
            if self._type_requires_nettype and not var.is_const:
                # w("wire ")
                pass
            is_array = False
        else:
            trnt = self._type_requires_nettype
            try:
                if var.is_const:
                    self._type_requires_nettype = False
                reg2 = self.out
                f2 = io.StringIO()
                self.out = f2

                t, array_dims = collect_array_dims(t)
                base_t, width, is_signed, _ = get_wire_t_params(t)
                if width is not None:
                    self.visit_iHdlExpr(width)
                    width = f2.getvalue()
                else:
                    width = 1

                is_array = len(array_dims) > 0

            finally:
                self.out = reg2
                self._type_requires_nettype = trnt

                nums = extract_numbers(f2.getvalue())
                sub = str(abs(int(nums[0]) - int(nums[1])) + 1)
                w(f'[{sub}:]')
                width = sub

        if not var.is_const:
            w(')')

        if is_array:
            self.visit_type_array_part(t)

        w("\n")

        self.out = reg
        # w = self.out.write
        self.out.write(f.getvalue())
        array_dims = len(array_dims)
        save_port_dims(name, width, array_dims)

        return True

    def visit_map_item(self, item):
        if isinstance(item, HdlOp)\
                and item.fn == HdlOpType.MAP_ASSOCIATION:
            w = self.out.write
            # k, v pair
            k, v = item.ops
            self.visit_iHdlExpr(k)
            w("=")
            self.visit_iHdlExpr(v)
        else:
            self.visit_iHdlExpr(item)

    def visit_map(self, map_):
        w = self.out.write
        with Indent(self.out):
            for last, m in iter_with_last(map_):
                self.visit_map_item(m)
                if last:
                    w("\n")
                else:
                    w(",\n")

    def visit_HdlCompInst(self, c):
        """
        :type c: HdlCompInst
        """
        self.visit_doc(c)
        w = self.out.write
        assert c.module_name
        w(c.name.val)
        w(' = ')
        self.visit_iHdlExpr(c.module_name)
        gms = c.param_map
        pms = c.port_map
        if pms:
            w("(\n")
            self.visit_map(pms)
            if gms:
                self.visit_map(gms)
            w(")")
        w("\n")
        return True

    def visit_HdlFunctionDef(self, o):
        """
        :type o: HdlFunctionDef
        """
        self.visit_doc(o)
        w = self.out.write
        if o.is_task:
            w("task ")
        else:
            w("function ")
        if not o.is_static:
            w("automatic ")

        if not o.is_task:
            trnt = self._type_requires_nettype
            try:
                self._type_requires_nettype = False
                self.visit_type_first_part(o.return_t)
                self.visit_type_array_part(o.return_t)
            finally:
                self._type_requires_nettype = trnt
        if o.is_virtual or o.is_operator:
            raise NotImplementedError(o)
        if not o.is_task and o.return_t is not HdlTypeAuto:
            # because " " is already written by previous string
            w(" ")
        w(o.name)
        ps = o.params
        trnt = self._type_requires_nettype
        try:
            self._type_requires_nettype = False
            if ps:
                w(" (\n")
                with Indent(self.out):
                    for last, p in iter_with_last(ps):
                        self.visit_port_declr(p)
                        if last:
                            w("\n")
                        else:
                            w(",\n")
                w(")")
            w(";\n")
        finally:
            self._type_requires_nettype = trnt
        with Indent(self.out):
            for s in o.body:
                if isinstance(s, HdlIdDef):
                    self.visit_HdlIdDef(s)
                    w(";\n")
                elif isinstance(s, iHdlStatement):
                    need_semi = self.visit_iHdlStatement(s)
                    if need_semi:
                        w(";\n")
                    else:
                        w("\n")
                else:
                    self.visit_iHdlExpr(s)
                    w(";\n")
        if o.is_task:
            w("endtask")
        else:
            w("endfunction")

    def visit_HdlClassDef(self, o):
        raise NotImplementedError()

    def visit_HdlPhysicalDef(self, o):
        raise NotImplementedError()

    def visit_HdlEnumDef(self, o):
        raise NotImplementedError()

    def visit_HdlModuleDec(self, e):
        raise ValueError(self, "does not support a module headers without body")

    def visit_HdlModuleDef(self, a):
        """
        :type a: HdlModuleDef
        """
        mod_dec = a.dec
        assert mod_dec is not None, a
        assert not mod_dec.objs, mod_dec
        self.visit_doc(mod_dec)
        w = self.out.write
        if not self.module:
            self.module = True
            w("from myhdl import *\n")
            w("\n")
        w("@block\n")
        w("def ")
        w(mod_dec.name)
        set_cur_module(mod_dec.name)
        # parameters and ports
        gs = mod_dec.params
        ps = mod_dec.ports
        # ports
        if ps:
            w(" (\n")
            with Indent(self.out):
                for last, p in iter_with_last(ps):
                    self.visit_port_declr(p)
                    if last:
                        if not gs:
                            w("\n")
                        else:
                            w(",\n")
                    else:
                        w(",\n")

        # params
        if gs:
            with Indent(self.out):
                for last, g in iter_with_last(gs):
                    self.visit_generic_declr(g)
                    if last:
                        w("\n")
                    else:
                        w(",\n")

        w(")")
        w(":\n")


        definition = [o for o in a.objs if isinstance(o, HdlIdDef)]
        inst = [o for o in a.objs if isinstance(o, HdlCompInst)]
        statement = [o for o in a.objs if isinstance(o, iHdlStatement)]
        # func = [o for o in a.objs if isinstance(o, HdlFunctionDef)]
        comb_statement = []
        seq_statement = []
        for s in statement:
            is_assign = self._visit_call_dispatch_dict.get(s.__class__)
            if is_assign.__name__ == 'visit_HdlStmAssign':
                comb_statement.append(s)
            else:
                seq_statement.append(s)

        with Indent(self.out):
            for d in definition:
                self.visit_HdlIdDef(d)
            w("\n")

            if comb_statement:
                assign_count = 0
                for c in comb_statement:
                    w("@always_comb\n")
                    w(f"def assign_{assign_count}():\n")
                    with Indent(self.out):
                        self.visit_HdlStmAssign(c)
                        # self.visit_iHdlStatement(c)
                        w("\n")
                    assign_count += 1

            for s in seq_statement:
                self.visit_iHdlStatement(s)
                # self.visit_HdlStmProcess(s)
                w("\n")

            for i in inst:
                self.visit_HdlCompInst(i)

        #     for f in func:
        #         self.visit_HdlFunctionDef(f)

            w("return instances()\n")
