from hdlConvertorAst.hdlAst import HdlOpType, HdlValueId, HdlValueInt, HdlAll, \
    HdlOp, HdlTypeAuto
from hdlConvertorAst.py_ver_compatibility import is_str
from hdlConvertorAst.to.common import ToHdlCommon, ASSOCIATIVITY, \
    ASSIGN_OPERATORS_SYMBOLS_C
from hdlConvertorAst.to.hdlUtils import iter_with_last
from hdlConvertorAst.to.myhdl.utils import collect_array_dims, get_wire_t_params
from hdlConvertorAst.to.myhdl.utils import filter_, search_from_dict, get_width_msg, find_colon
import io

L = ASSOCIATIVITY.L_TO_R
R = ASSOCIATIVITY.R_TO_L

ASSIGN_OPERATORS = [
    HdlOpType.ASSIGN,
    HdlOpType.PLUS_ASSIGN,
    HdlOpType.MINUS_ASSIGN,
    HdlOpType.MUL_ASSIGN,
    HdlOpType.DIV_ASSIGN,
    HdlOpType.MOD_ASSIGN,
    HdlOpType.AND_ASSIGN,
    HdlOpType.OR_ASSIGN,
    HdlOpType.XOR_ASSIGN,
    HdlOpType.SHIFT_LEFT_ASSIGN,
    HdlOpType.SHIFT_RIGHT_ASSIGN,
    HdlOpType.ARITH_SHIFT_LEFT_ASSIGN,
    HdlOpType.ARITH_SHIFT_RIGHT_ASSIGN,
]

SIGNED = HdlValueId("signed")


def pop_signed_flag(o):
    """
    :type op: HdlOp

    pop signed/unsigned flag from type expr
    """
    base_expr = o
    is_signed = None

    if o.fn == HdlOpType.PARAMETRIZATION and len(o.ops) == 2:
        op1 = o.ops[1]
        if isinstance(op1, HdlOp) and\
                op1.fn == HdlOpType.MAP_ASSOCIATION and\
                op1.ops[0] == SIGNED:
            base_expr = o.ops[0]
            is_signed = bool(int(op1.ops[1]))

    return base_expr, is_signed


class ToMyhdlExpr(ToHdlCommon):

    GENERIC_BIN_OPS = {
        HdlOpType.APOSTROPHE: "'",

        HdlOpType.AND: " & ",
        HdlOpType.AND_LOG: " and ",
        HdlOpType.OR: " | ",
        HdlOpType.OR_LOG: " or ",
        HdlOpType.NAND: " ~& ",
        HdlOpType.NOR: " ~| ",
        HdlOpType.XOR: " ^ ",
        HdlOpType.XNOR: " ~^ ",

        HdlOpType.DIV: " / ",
        HdlOpType.POW: " ** ",
        HdlOpType.MOD: " % ",

        HdlOpType.EQ: ' == ',
        HdlOpType.NE: " != ",
        HdlOpType.IS: ' === ',
        HdlOpType.IS_NOT: " !== ",

        HdlOpType.EQ_MATCH:" ==? ",
        HdlOpType.NE_MATCH:" !=? ",

        HdlOpType.SLL: " << ",
        HdlOpType.SRL: " >> ",

        HdlOpType.SLA: " << ",
        HdlOpType.SRA: " >> ",

        HdlOpType.DOWNTO: ":",
        HdlOpType.TO: ":",
        HdlOpType.PART_SELECT_POST: " +: ",
        HdlOpType.PART_SELECT_PRE: " -: ",
        HdlOpType.MAP_ASSOCIATION: ":",

        HdlOpType.ARITH_SHIFT_LEFT_ASSIGN: ' <<= ',
        HdlOpType.ARITH_SHIFT_RIGHT_ASSIGN: ' >>= ',
        HdlOpType.DOUBLE_COLON: "::",
    }
    GENERIC_BIN_OPS.update(ToHdlCommon.GENERIC_BIN_OPS)
    GENERIC_BIN_OPS.update(ASSIGN_OPERATORS_SYMBOLS_C)

    OP_PRECEDENCE = {
        HdlOpType.APOSTROPHE: (1, L),
        HdlOpType.DOT: (1, L),
        HdlOpType.INDEX: (1, L),

        HdlOpType.CALL: (2, L),
        HdlOpType.TYPE_OF: (2, L),
        HdlOpType.PARAMETRIZATION: (2, L),

        HdlOpType.POW: (5, L),

        HdlOpType.CONCAT: (6, L),

        HdlOpType.REPL_CONCAT: (7, L),

        HdlOpType.DIV: (8, L),
        HdlOpType.MUL: (8, L),
        HdlOpType.MOD: (8, L),

        HdlOpType.ADD: (9, L),
        HdlOpType.SUB: (9, L),

        HdlOpType.SLL: (10, L),
        HdlOpType.SRL: (10, L),
        HdlOpType.SLA: (10, L),
        HdlOpType.SRA: (10, L),

        HdlOpType.GT: (11, L),
        HdlOpType.LT: (11, L),
        HdlOpType.GE: (11, L),
        HdlOpType.LE: (11, L),

        HdlOpType.EQ: (12, L),
        HdlOpType.NE: (12, L),
        HdlOpType.IS: (12, L),
        HdlOpType.IS_NOT: (12, L),
        HdlOpType.EQ_MATCH: (12, L),
        HdlOpType.NE_MATCH: (12, L),

        HdlOpType.AND: (13, L),
        HdlOpType.XOR: (13, L),
        HdlOpType.OR: (13, L),
        HdlOpType.NAND: (13, L),
        HdlOpType.XNOR: (13, L),

        HdlOpType.AND_LOG: (14, L),
        HdlOpType.OR_LOG: (14, L),

        HdlOpType.TERNARY: (15, R),

        HdlOpType.RISING: (16, R),
        HdlOpType.FALLING: (16, R),
        HdlOpType.DOWNTO: (17, L),
        HdlOpType.TO: (17, L),
        HdlOpType.PART_SELECT_PRE: (17, L),
        HdlOpType.PART_SELECT_POST: (17, L),
        HdlOpType.MAP_ASSOCIATION: (17, L),

    }
    OP_PRECEDENCE.update({k: (3, R) for k in [
        HdlOpType.MINUS_UNARY,
        HdlOpType.PLUS_UNARY,
        HdlOpType.INCR_PRE,
        HdlOpType.INCR_POST,
        HdlOpType.DECR_PRE,
        HdlOpType.DECR_POST,
        HdlOpType.NEG,
        HdlOpType.NEG_LOG,
        HdlOpType.OR_UNARY,
        HdlOpType.AND_UNARY,
        HdlOpType.NAND_UNARY,
        HdlOpType.NOR_UNARY,
        HdlOpType.XOR_UNARY,
        HdlOpType.XNOR_UNARY
    ]})
    OP_PRECEDENCE.update({k: (18, ASSOCIATIVITY.NONE)
                          for k in ASSIGN_OPERATORS})

    GENERIC_UNARY_OPS = {
        HdlOpType.NEG_LOG: "not ",
        HdlOpType.NEG: "~",
        HdlOpType.MINUS_UNARY: "-",
        HdlOpType.PLUS_UNARY: "+",
        HdlOpType.OR_UNARY: "|",
        HdlOpType.AND_UNARY: "&",
        HdlOpType.NAND_UNARY: "~&",
        HdlOpType.NOR_UNARY: "~|",
        HdlOpType.XOR_UNARY: "^",
        HdlOpType.XNOR_UNARY: "~^",
        HdlOpType.RISING: ".posedge",
        HdlOpType.FALLING: ".negedge",
        HdlOpType.INCR_PRE: "++",
        HdlOpType.DECR_PRE: "--",
    }
    GENERIC_UNARY_OPS_POSTFIX = {
        HdlOpType.INCR_POST: " += 1",
        HdlOpType.DECR_POST: " -= 1",
    }

    def visit_HdlValueInt(self, o):
        """
        :type o: HdlValueInt
        """
        w = self.out.write
        if o.bits is None:
            w(str(o.val))
        else:
            if o.base is None:
                f = "0x{0:x}"
            else:
                b = o.base
                if b == 2:
                    base_char = '0b'
                elif b == 8:
                    base_char = '0O'
                elif b == 10:
                    base_char = ''
                elif b == 16:
                    base_char = '0x'
                else:
                    raise NotImplementedError(b)
                f = base_char + "{0}"
            w(f.format(o.val))
        return o.bits

    def visit_iHdlExpr(self, o):
        """
        :type o: iHdlExpr
        :return: True, the flag used to mark that the ; should be added if this is a statement
        """
        w = self.out.write
        if isinstance(o, HdlValueId):
            w(o.val)
        elif is_str(o):
            w('"%s"' % o.replace("\n", "\\\n"))
        elif isinstance(o, HdlValueInt):
            return self.visit_HdlValueInt(o)
        elif isinstance(o, HdlOp):
            _o, is_signed = pop_signed_flag(o)
            if o is not _o:
                self.visit_iHdlExpr(_o)
            else:
                self.visit_HdlOp(_o)

            if is_signed is True:
                w(".signed()")
            # elif is_signed is False:
            #     w(" unsigned")
        elif o is HdlAll:
            w("_comb")
        elif o is HdlTypeAuto:
            pass
        elif o is None:
            w("None")
        elif isinstance(o, float):
            w(str(o))
        # elif isinstance(o, list):
        #     w("'{")
        #     for last, e in iter_with_last(o):
        #         self.visit_iHdlExpr(e)
        #         if not last:
        #             w(", ")
        #     w("}")
        else:
            raise NotImplementedError(o.__class__, o)
        return True

    def _visit_operand(self, operand, i,
                           parent,
                           expr_requires_parenthesis,
                           cancel_parenthesis):

        if isinstance(operand, HdlOp) and \
               (operand.fn in self.GENERIC_UNARY_OPS or operand.fn in self.GENERIC_UNARY_OPS_POSTFIX) and \
               (parent.fn in self.GENERIC_UNARY_OPS or parent.fn in self.GENERIC_UNARY_OPS_POSTFIX):
            # unary operator in unary operator
            expr_requires_parenthesis = True

        # return super(ToMyhdlExpr, self)._visit_operand(operand, i,
        #                    parent,
        #                    expr_requires_parenthesis,
        #                    cancel_parenthesis)
        use_parenthesis = False
        if not cancel_parenthesis:
            # resolve if the parenthesis are required
            precedence_my, asoc_my, op_my = self._precedence_of_expr(operand)
            if precedence_my >= 0:  # if this is an expression
                if expr_requires_parenthesis or asoc_my is ASSOCIATIVITY.NONE:
                    use_parenthesis = True
                else:
                    precedence_parent, asoc_parent = self.OP_PRECEDENCE[parent.fn]
                    right = None
                    left = None
                    argc = len(parent.ops)
                    assert argc, parent
                    if argc == 1:
                        if asoc_parent == ASSOCIATIVITY.L_TO_R:
                            # post fix
                            left = parent.ops[0]
                        else:
                            assert asoc_parent == ASSOCIATIVITY.R_TO_L, asoc_parent
                            right = parent.ops[0]
                    else:
                        if i == 0:
                            right = parent.ops[1]
                        else:
                            left = parent.ops[i - 1]
                            if argc > i + 2:
                                right = parent.ops[i + 1]

                    if self._visit_operand_parentheses_extra_check(
                            op_my, precedence_my, asoc_my, parent.fn,
                            precedence_parent, asoc_parent, left, right):
                        use_parenthesis = True
                    else:
                        if left is not None:  # "operand" is on right side of parent operator
                            # same precedence -> parenthesis on right (this) if it is expression
                            # a + (b + c)
                            # a + b + c = (a + b) + c
                            # right with lower precedence -> parenthesis for right not required
                            # a + b * c = a + (b * c)
                            # right with higher precedence -> parenthesis for right
                            # a * (b + c)
                            if precedence_my > precedence_parent:
                                use_parenthesis = True
                            elif precedence_my == precedence_parent:
                                use_parenthesis = argc != 1 or asoc_parent != ASSOCIATIVITY.L_TO_R

                        if not use_parenthesis and right is not None:
                            # "operand" is on left side of parent operator
                            # if op_my == parent.fn:
                            #    right_prec, _, right_op = self._precedence_of_expr(right)
                            #    if right_op == op_my:
                            #        # right and left with same precedence -> parenthesis on both sides
                            #        # (a + b) + (c + d)
                            #        use_parenthesis = True
                            if precedence_my > precedence_parent:
                                # left with higher precedence -> parenthesis for left
                                # (a + b) * c
                                # a + b + c + d = (a + b) + c + d
                                # = ((a + b) + c) + d
                                use_parenthesis = True
        w = self.out.write
        if use_parenthesis:
            w("(")
        x = self.visit_iHdlExpr(operand)
        if use_parenthesis:
            w(")")
        return x

    def visit_HdlOp(self, o):
        """
        :type o: HdlOp
        """
        w = self.out.write
        op = o.fn
        if op == HdlOpType.CONCAT:
            w = self.out.write
            reg = self.out
            f_ = io.StringIO()
            self.out = f_
            w("concat(")
            for is_last, (o_i, _o) in iter_with_last(enumerate(o.ops)):
                f_.truncate(0)
                f_.seek(0)
                x = self._visit_operand(_o, o_i, o, False, True)

                if isinstance(x, int) and not isinstance(x, bool):
                    w(f"modbv({f_.getvalue()})[{x}:]")
                else:
                    s_ = f_.getvalue()
                    if s_[0] == '~':
                        w(f"modbv({s_})[len({s_[1:]}):]")
                    else:
                        w(s_)

                if not is_last:
                    w(", ")

            w(")")
            self.out = reg
            return
        elif op == HdlOpType.REPL_CONCAT:
            w = self.out.write
            w("concat(")
            reg = self.out
            f_ = io.StringIO()
            self.out = f_

            self._visit_operand(o.ops[0], 0, o, True, False)
            cnt = f_.getvalue()
            w('*[')

            w("concat(")
            f_.truncate(0)
            f_.seek(0)
            for is_last, (o_i, _o) in iter_with_last(enumerate(o.ops[1:])):
                f_.truncate(0)
                f_.seek(0)
                x = self._visit_operand(_o, o_i, o, False, True)
                if isinstance(x, int) and not isinstance(x, bool):
                    w(f"modbv({f_.getvalue()})[{x}:]")
                else:
                    s_ = f_.getvalue()
                    if s_[0] == '~':
                        w(f"modbv({s_})[len({s_[1:]}):]")
                    else:
                        w(s_)
                if not is_last:
                    w(", ")
            w(')')

            w(f' for _ in range({cnt})]')
            w(")")
            self.out = reg
            return
        elif op == HdlOpType.TERNARY:
            cond, v0, v1 = o.ops
            self._visit_operand(v0, 1, o, False, False)
            w(" if ")
            self._visit_operand(cond, 0, o, True, False)
            w(" else ")
            self._visit_operand(v1, 2, o, False, False)
            return
        elif op == HdlOpType.TYPE_OF:
            w("type(")
            self._visit_operand(o.ops[0], 0, o, False, True)
            w(")")
            return
        elif op == HdlOpType.RISING:
            self._visit_operand(o.ops[0], 0, o, False, True)
            w('.posedge')
            return
        elif op == HdlOpType.FALLING:
            self._visit_operand(o.ops[0], 0, o, False, True)
            w('.negedge')
            return
        elif op == HdlOpType.INCR_PRE:
            self._visit_operand(o.ops[0], 0, o, False, True)
            w(' += 1')
            return
        elif op == HdlOpType.DECR_PRE:
            self._visit_operand(o.ops[0], 0, o, False, True)
            w(' -= 1')
            return
        elif op == HdlOpType.ASSIGN:
            f = io.StringIO()
            reg = self.out
            self.out = f
            self._visit_operand(o.ops[0], 0, o, False, True)
            dst = f.getvalue()
            f.truncate(0)
            f.seek(0)
            self._visit_operand(o.ops[1], 0, o, False, True)
            src = f.getvalue()

            res = filter_(dst)
            if res[0] == 'var':
                w(f'{res[1]}.next')
                w(' = ')
                w(src)
            elif res[0] == 'array':
                dims = search_from_dict(res[1])[1]
                w(f'{res[1]}')
                if len(res[2]) <= dims:
                    for i in res[2]:
                        w(f'[{i}]')
                    w('.next')
                else:
                    for i in range(dims):
                        w(f'[{res[2][i]}]')
                    w('.next')
                    for i in range(dims, len(res[2])):
                        w(f'[{res[2][i]}]')
                w(' = ')
                w(src)
            elif res[0] == 'func':
                w('tmp = ')
                w(src)
                w('\n')
                widths = []
                names = []
                for elem in res[2]:
                    msg = filter_(elem)
                    if msg[0] == 'var':
                        type_, name_ = msg
                        width = search_from_dict(name_)[0]
                        name_ += '.next'

                    elif msg[0] == 'array':
                        type_, name_, idx_ = msg
                        dim = search_from_dict(name_)[1]
                        if len(idx_) == dim:
                            width = search_from_dict(name_)[0]
                            for idx in idx_:
                                name_ += f'[{idx}]'
                            name_ += '.next'

                        elif len(idx_) == dim + 1:
                            width = get_width_msg(idx_[-1])
                            for i in range(len(idx_)-1):
                                name_ += f'[{idx_[i]}]'
                            name_ += '.next'
                            name_ += f'[{idx_[-1]}]'
                        else:
                            raise ValueError(f"len: {len(idx_)} != dim or dim + 1")

                    widths.append(width)
                    names.append(name_)

                start = '0'
                for i in range(len(widths) - 1, -1, -1):
                    w(f'{names[i]}')
                    w(' = ')
                    w(f'tmp[{widths[i]}+{start}:{start}]\n')
                    start = f'{widths[i]}+{start}'

            self.out = reg
            return
        elif op == HdlOpType.INDEX:
            op0, op1 = o.ops
            w = self.out.write
            reg = self.out
            f = io.StringIO()
            self.out = f
            self._visit_operand(op0, 0, o, False, False)
            s1 = f.getvalue()
            w(s1)
            w("[")
            f.truncate(0)
            f.seek(0)
            self._visit_operand(op1, 1, o, False, True)
            s2 = f.getvalue()
            idx = find_colon(s2)
            if idx is not None:
                a, b = s2[0:idx], s2[idx+1:]
                w(f"{a} + 1:{b}")
            else:
                w(s2)
            self.out = reg
            w("]")
            return
        elif op == HdlOpType.DOWNTO:
            self._visit_operand(o.ops[0], 0, o, False, True)
            w(':')
            self._visit_operand(o.ops[1], 0, o, False, True)
            return
        elif op == HdlOpType.SRA:
            self._visit_operand(o.ops[0], 0, o, False, True)
            w(' >> ')
            self._visit_operand(o.ops[1], 0, o, False, True)
            reg = self.out
            f = io.StringIO()
            self.out = f
            self._visit_operand(o.ops[0], 0, o, False, True)
            w(f' | {f.getvalue()}[len({f.getvalue()}) - 1] << len({f.getvalue()}) - 1')
            self.out = reg
            return

        elif op == HdlOpType.PLUS_ASSIGN:
            f = io.StringIO()
            reg = self.out
            self.out = f
            self._visit_operand(o.ops[0], 0, o, False, True)
            dst = f.getvalue()
            f.truncate(0)
            f.seek(0)
            self._visit_operand(o.ops[1], 0, o, False, True)
            src = f.getvalue()

            res = filter_(dst)
            if res[0] == 'var':
                w(f'{res[1]}.next')
                w(' += ')
                w(src)
            elif res[0] == 'array':
                dims = search_from_dict(res[1])[1]
                w(f'{res[1]}')
                if len(res[2]) <= dims:
                    for i in res[2]:
                        w(f'[{i}]')
                    w('.next')
                else:
                    for i in range(dims):
                        w(f'[{res[2][i]}]')
                    w('.next')
                    for i in range(dims, len(res[2])):
                        w(f'[{res[2][i]}]')
                w(' += ')
                w(src)

            self.out = reg
            return
        elif op == HdlOpType.MINUS_ASSIGN:
            f = io.StringIO()
            reg = self.out
            self.out = f
            self._visit_operand(o.ops[0], 0, o, False, True)
            dst = f.getvalue()
            f.truncate(0)
            f.seek(0)
            self._visit_operand(o.ops[1], 0, o, False, True)
            src = f.getvalue()

            res = filter_(dst)
            if res[0] == 'var':
                w(f'{res[1]}.next')
                w(' -= ')
                w(src)
            elif res[0] == 'array':
                dims = search_from_dict(res[1])[1]
                w(f'{res[1]}')
                if len(res[2]) <= dims:
                    for i in res[2]:
                        w(f'[{i}]')
                    w('.next')
                else:
                    for i in range(dims):
                        w(f'[{res[2][i]}]')
                    w('.next')
                    for i in range(dims, len(res[2])):
                        w(f'[{res[2][i]}]')
                w(' -= ')
                w(src)

            self.out = reg
            return
        elif op == HdlOpType.MUL_ASSIGN:
            f = io.StringIO()
            reg = self.out
            self.out = f
            self._visit_operand(o.ops[0], 0, o, False, True)
            dst = f.getvalue()
            f.truncate(0)
            f.seek(0)
            self._visit_operand(o.ops[1], 0, o, False, True)
            src = f.getvalue()

            res = filter_(dst)
            if res[0] == 'var':
                w(f'{res[1]}.next')
                w(' *= ')
                w(src)
            elif res[0] == 'array':
                dims = search_from_dict(res[1])[1]
                w(f'{res[1]}')
                if len(res[2]) <= dims:
                    for i in res[2]:
                        w(f'[{i}]')
                    w('.next')
                else:
                    for i in range(dims):
                        w(f'[{res[2][i]}]')
                    w('.next')
                    for i in range(dims, len(res[2])):
                        w(f'[{res[2][i]}]')
                w(' *= ')
                w(src)

            self.out = reg
            return
        elif op == HdlOpType.DIV_ASSIGN:
            f = io.StringIO()
            reg = self.out
            self.out = f
            self._visit_operand(o.ops[0], 0, o, False, True)
            dst = f.getvalue()
            f.truncate(0)
            f.seek(0)
            self._visit_operand(o.ops[1], 0, o, False, True)
            src = f.getvalue()

            res = filter_(dst)
            if res[0] == 'var':
                w(f'{res[1]}.next')
                w(' /= ')
                w(src)
            elif res[0] == 'array':
                dims = search_from_dict(res[1])[1]
                w(f'{res[1]}')
                if len(res[2]) <= dims:
                    for i in res[2]:
                        w(f'[{i}]')
                    w('.next')
                else:
                    for i in range(dims):
                        w(f'[{res[2][i]}]')
                    w('.next')
                    for i in range(dims, len(res[2])):
                        w(f'[{res[2][i]}]')
                w(' /= ')
                w(src)

            self.out = reg
            return
        elif op == HdlOpType.MOD_ASSIGN:
            f = io.StringIO()
            reg = self.out
            self.out = f
            self._visit_operand(o.ops[0], 0, o, False, True)
            dst = f.getvalue()
            f.truncate(0)
            f.seek(0)
            self._visit_operand(o.ops[1], 0, o, False, True)
            src = f.getvalue()

            res = filter_(dst)
            if res[0] == 'var':
                w(f'{res[1]}.next')
                w(' %= ')
                w(src)
            elif res[0] == 'array':
                dims = search_from_dict(res[1])[1]
                w(f'{res[1]}')
                if len(res[2]) <= dims:
                    for i in res[2]:
                        w(f'[{i}]')
                    w('.next')
                else:
                    for i in range(dims):
                        w(f'[{res[2][i]}]')
                    w('.next')
                    for i in range(dims, len(res[2])):
                        w(f'[{res[2][i]}]')
                w(' %= ')
                w(src)

            self.out = reg
            return
        elif op == HdlOpType.AND_ASSIGN:
            f = io.StringIO()
            reg = self.out
            self.out = f
            self._visit_operand(o.ops[0], 0, o, False, True)
            dst = f.getvalue()
            f.truncate(0)
            f.seek(0)
            self._visit_operand(o.ops[1], 0, o, False, True)
            src = f.getvalue()

            res = filter_(dst)
            if res[0] == 'var':
                w(f'{res[1]}.next')
                w(' &= ')
                w(src)
            elif res[0] == 'array':
                dims = search_from_dict(res[1])[1]
                w(f'{res[1]}')
                if len(res[2]) <= dims:
                    for i in res[2]:
                        w(f'[{i}]')
                    w('.next')
                else:
                    for i in range(dims):
                        w(f'[{res[2][i]}]')
                    w('.next')
                    for i in range(dims, len(res[2])):
                        w(f'[{res[2][i]}]')
                w(' &= ')
                w(src)

            self.out = reg
            return
        elif op == HdlOpType.OR_ASSIGN:
            f = io.StringIO()
            reg = self.out
            self.out = f
            self._visit_operand(o.ops[0], 0, o, False, True)
            dst = f.getvalue()
            f.truncate(0)
            f.seek(0)
            self._visit_operand(o.ops[1], 0, o, False, True)
            src = f.getvalue()

            res = filter_(dst)
            if res[0] == 'var':
                w(f'{res[1]}.next')
                w(' |= ')
                w(src)
            elif res[0] == 'array':
                dims = search_from_dict(res[1])[1]
                w(f'{res[1]}')
                if len(res[2]) <= dims:
                    for i in res[2]:
                        w(f'[{i}]')
                    w('.next')
                else:
                    for i in range(dims):
                        w(f'[{res[2][i]}]')
                    w('.next')
                    for i in range(dims, len(res[2])):
                        w(f'[{res[2][i]}]')
                w(' |= ')
                w(src)

            self.out = reg
            return
        elif op == HdlOpType.XOR_ASSIGN:
            f = io.StringIO()
            reg = self.out
            self.out = f
            self._visit_operand(o.ops[0], 0, o, False, True)
            dst = f.getvalue()
            f.truncate(0)
            f.seek(0)
            self._visit_operand(o.ops[1], 0, o, False, True)
            src = f.getvalue()

            res = filter_(dst)
            if res[0] == 'var':
                w(f'{res[1]}.next')
                w(' ^= ')
                w(src)
            elif res[0] == 'array':
                dims = search_from_dict(res[1])[1]
                w(f'{res[1]}')
                if len(res[2]) <= dims:
                    for i in res[2]:
                        w(f'[{i}]')
                    w('.next')
                else:
                    for i in range(dims):
                        w(f'[{res[2][i]}]')
                    w('.next')
                    for i in range(dims, len(res[2])):
                        w(f'[{res[2][i]}]')
                w(' ^= ')
                w(src)

            self.out = reg
            return
        elif op == HdlOpType.SHIFT_LEFT_ASSIGN:
            f = io.StringIO()
            reg = self.out
            self.out = f
            self._visit_operand(o.ops[0], 0, o, False, True)
            dst = f.getvalue()
            f.truncate(0)
            f.seek(0)
            self._visit_operand(o.ops[1], 0, o, False, True)
            src = f.getvalue()

            res = filter_(dst)
            if res[0] == 'var':
                w(f'{res[1]}.next')
                w(' <<= ')
                w(src)
            elif res[0] == 'array':
                dims = search_from_dict(res[1])[1]
                w(f'{res[1]}')
                if len(res[2]) <= dims:
                    for i in res[2]:
                        w(f'[{i}]')
                    w('.next')
                else:
                    for i in range(dims):
                        w(f'[{res[2][i]}]')
                    w('.next')
                    for i in range(dims, len(res[2])):
                        w(f'[{res[2][i]}]')
                w(' <<= ')
                w(src)

            self.out = reg
            return
        elif op == HdlOpType.SHIFT_RIGHT_ASSIGN:
            f = io.StringIO()
            reg = self.out
            self.out = f
            self._visit_operand(o.ops[0], 0, o, False, True)
            dst = f.getvalue()
            f.truncate(0)
            f.seek(0)
            self._visit_operand(o.ops[1], 0, o, False, True)
            src = f.getvalue()

            res = filter_(dst)
            if res[0] == 'var':
                w(f'{res[1]}.next')
                w(' >>= ')
                w(src)
            elif res[0] == 'array':
                dims = search_from_dict(res[1])[1]
                w(f'{res[1]}')
                if len(res[2]) <= dims:
                    for i in res[2]:
                        w(f'[{i}]')
                    w('.next')
                else:
                    for i in range(dims):
                        w(f'[{res[2][i]}]')
                    w('.next')
                    for i in range(dims, len(res[2])):
                        w(f'[{res[2][i]}]')
                w(' >>= ')
                w(src)

            self.out = reg
            return
        elif op == HdlOpType.ARITH_SHIFT_LEFT_ASSIGN:
            f = io.StringIO()
            reg = self.out
            self.out = f
            self._visit_operand(o.ops[0], 0, o, False, True)
            dst = f.getvalue()
            f.truncate(0)
            f.seek(0)
            self._visit_operand(o.ops[1], 0, o, False, True)
            src = f.getvalue()

            res = filter_(dst)
            if res[0] == 'var':
                w(f'{res[1]}.next')
                w(' >>= ')
                w(src)
            elif res[0] == 'array':
                dims = search_from_dict(res[1])[1]
                w(f'{res[1]}')
                if len(res[2]) <= dims:
                    for i in res[2]:
                        w(f'[{i}]')
                    w('.next')
                else:
                    for i in range(dims):
                        w(f'[{res[2][i]}]')
                    w('.next')
                    for i in range(dims, len(res[2])):
                        w(f'[{res[2][i]}]')
                w(' >>= ')
                w(src)

            self.out = reg
            return
        elif op == HdlOpType.ARITH_SHIFT_RIGHT_ASSIGN:
            f = io.StringIO()
            reg = self.out
            self.out = f
            self._visit_operand(o.ops[0], 0, o, False, True)
            dst = f.getvalue()
            f.truncate(0)
            f.seek(0)
            self._visit_operand(o.ops[1], 0, o, False, True)
            src = f.getvalue()

            res = filter_(dst)
            if res[0] == 'var':
                w(f'{res[1]}.next')
                w(' <<= ')
                w(src)
            elif res[0] == 'array':
                dims = search_from_dict(res[1])[1]
                w(f'{res[1]}')
                if len(res[2]) <= dims:
                    for i in res[2]:
                        w(f'[{i}]')
                    w('.next')
                else:
                    for i in range(dims):
                        w(f'[{res[2][i]}]')
                    w('.next')
                    for i in range(dims, len(res[2])):
                        w(f'[{res[2][i]}]')
                w(' <<= ')
                w(src)

            self.out = reg
            return
        elif op == HdlOpType.PART_SELECT_POST:
            reg = self.out
            f = io.StringIO()
            self.out = f
            self._visit_operand(o.ops[0], 0, o, False, True)
            ops0 = f.getvalue()
            f.truncate(0)
            f.seek(0)
            self._visit_operand(o.ops[1], 0, o, False, True)
            ops1 = f.getvalue()
            w(f'{ops0}+{ops1}-1:{ops0}')
            # print(f'{ops0}+{ops1}-1:{ops0}')
            self.out = reg
            return
        elif op == HdlOpType.PART_SELECT_PRE:
            reg = self.out
            f = io.StringIO()
            self.out = f
            self._visit_operand(o.ops[0], 0, o, False, True)
            ops0 = f.getvalue()
            f.truncate(0)
            f.seek(0)
            self._visit_operand(o.ops[1], 0, o, False, True)
            ops1 = f.getvalue()
            w(f'{ops0}:{ops0}-{ops1}+1')
            self.out = reg
            return
        elif op == HdlOpType.AND_UNARY:
            self._visit_operand(o.ops[0], 0, o, False, True)
            w(' == ')
            self._visit_operand(o.ops[0], 0, o, False, True)
            w('.max - 1')
            # h[3:0].max - 1 == h[3:0]
            return
        elif op == HdlOpType.OR_UNARY:
            self._visit_operand(o.ops[0], 0, o, False, True)
            w(' != 0')
            return
        elif op == HdlOpType.NAND_UNARY:
            self._visit_operand(o.ops[0], 0, o, False, True)
            w(' != ')
            self._visit_operand(o.ops[0], 0, o, False, True)
            w('.max - 1')
            return
        elif op == HdlOpType.NOR_UNARY:
            self._visit_operand(o.ops[0], 0, o, False, True)
            w(' == 0')
            return
        elif op == HdlOpType.XOR_UNARY:
            w('bin(')
            self._visit_operand(o.ops[0], 0, o, False, True)
            w(').count(\'1\') % 2 == 1')
            return
        elif op == HdlOpType.XNOR_UNARY:
            w('bin(')
            self._visit_operand(o.ops[0], 0, o, False, True)
            w(').count(\'1\') % 2 == 0')
            return
        elif op == HdlOpType.CALL:
            # print(o.ops[0], type(o.ops[0]))
            if o.ops[0].val == '$signed':
                w('(')
                self._visit_operand(o.ops[1], 0, o, False, True)
                w(')')
                w('.signed()')
            return
        else:
            super(ToMyhdlExpr, self).visit_HdlOp(o)
        return True

    def visit_type_first_part(self, t):
        """
        :type t: iHdlExpr
        :return: True if the type has also the array dimension part
        """
        w = self.out.write
        t, array_dims = collect_array_dims(t)
        wire_params = get_wire_t_params(t)
        if wire_params is None:
            pass
            # if t != HdlTypeAuto:
            #     if isinstance(t, HdlOp) and t.fn == HdlOpType.TYPE_OF:
            #         w("var ")
            #     self.visit_iHdlExpr(t)
            # elif self._type_requires_nettype:
            #     w("wire")
        else:
            base_t, width, is_signed, _ = wire_params
            # space_required = False
            # if base_t is not HdlTypeAuto and base_t:
            #     if not (not self._type_requires_nettype and base_t in (HdlValueId("wire"), HdlValueId("reg"))):
            #         w(base_t.val)
            #         space_required = True
            # elif self._type_requires_nettype:
            #     w("wire")
            #     space_required = True

            # if is_signed is None:
            #     pass
            # else:
            #     if space_required:
            #         w(" ")
            #     if is_signed:
            #         w("signed")
            #     else:
            #         w("unsigned")

            if width is not None:
                # 1D vector
                w("[")
                self.visit_iHdlExpr(width)
                w("]")
            else:
                w('[1:0]')

        return len(array_dims) > 0

    def visit_type_array_part(self, t):
        """
        :type t: iHdlExpr
        """
        w = self.out.write
        f = self.out
        _, array_dim = collect_array_dims(t)
        for ad in array_dim:
            element = f.getvalue()
            f.seek(0)
            w("[")
            w(element)
            if ad is not None:
                # ad.fn == HdlOpType.DOWNTO/TO
                f2 = io.StringIO()
                reg = self.out
                self.out = f2

                self.visit_iHdlExpr(ad.ops[0])
                upper = f2.getvalue()
                f2.truncate(0)
                f2.seek(0)
                self.visit_iHdlExpr(ad.ops[1])
                lower = f2.getvalue()
                w(f' for _ in range(abs(({upper}) - ({lower}))+1)')
                # self.visit_iHdlExpr(ad)

                self.out = reg
            w("]")
