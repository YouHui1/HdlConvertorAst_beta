from hdlConvertorAst.hdlAst import HdlOpType, HdlStmWait, HdlStmBlock,\
    HdlStmProcessTriggerConstrain, HdlStmNop, HdlAll
from hdlConvertorAst.to.hdlUtils import Indent, iter_with_last
from hdlConvertorAst.to.myhdl.expr import ToMyhdlExpr
import io
from hdlConvertorAst.to.myhdl.utils import filter_, search_from_dict, get_width_msg


class ToMyhdlStm(ToMyhdlExpr):
    ASSIGN_OPS = {
        HdlOpType.ASSIGN: '=',
        HdlOpType.PLUS_ASSIGN: '+=',
        HdlOpType.MINUS_ASSIGN: '-=',
        HdlOpType.MUL_ASSIGN: '*=',
        HdlOpType.DIV_ASSIGN: '/=',
        HdlOpType.MOD_ASSIGN: '%=',
        HdlOpType.AND_ASSIGN: '&=',
        HdlOpType.OR_ASSIGN: '|=',
        HdlOpType.XOR_ASSIGN: '^=',
        HdlOpType.SHIFT_LEFT_ASSIGN: '<<=',
        HdlOpType.SHIFT_RIGHT_ASSIGN: '>>=',
        HdlOpType.ARITH_SHIFT_LEFT_ASSIGN: '<<<=',
        HdlOpType.ARITH_SHIFT_RIGHT_ASSIGN: '>>>=',
    }

    def __init__(self, out_stream):
        super(ToMyhdlStm, self).__init__(out_stream)
        self.top_stm = None
        self.is_in_loop_spec = False
        self.state_counter = [0, 0, 0]

    def visit_hdlAttributes(self, o):
        """
        :type o: List[Tuple[str, Optional[iHdlExpr]]]
        """
        if not o:
            return
        w = self.out.write
        w("(* ")
        for last, (aId, aVal) in iter_with_last(o):
            w(aId)
            if aVal is not None:
                w("=")
                self.visit_iHdlExpr(aVal)

            if not last:
                w(", ")
        w(" *)")

    def visit_iHdlStatement(self, stm):
        """
        :type stm: iHdlStatement
        """
        if stm.hdlAttributes:
            self.visit_hdlAttributes(stm.hdlAttributes)
            self.out.write("\n")

        if self.top_stm is None:
            self.top_stm = stm
            try:
                visit_fn = self._visit_call_dispatch_dict.get(stm.__class__, None)
                if visit_fn is not None:
                    return visit_fn(stm)
                elif stm is None:
                    return self.visit_HdlStmNop(HdlStmNop())
                else:
                    return self.visit_iHdlExpr(stm)

                # return ToMyhdlExpr.visit_iHdlStatement(self, stm)
            finally:
                self.top_stm = None
        else:
            visit_fn = self._visit_call_dispatch_dict.get(stm.__class__, None)
            if visit_fn is not None:
                return visit_fn(stm)
            elif stm is None:
                return self.visit_HdlStmNop(HdlStmNop())
            else:
                return self.visit_iHdlExpr(stm)

            # return ToMyhdlExpr.visit_iHdlStatement(self, stm)

    def visit_HdlStmProcess(self, proc):
        """
        :type proc: HdlStmProcess
        """
        self.visit_doc(proc)
        sens = proc.sensitivity
        body = proc.body
        w = self.out.write
        skip_body = False
        if sens is None and proc.trigger_constrain is None:
            if isinstance(body, HdlStmWait):
                skip_body = True
                wait = body
                body = []
            elif (isinstance(body, HdlStmBlock)
                    and body.body
                    and isinstance(body.body[0], HdlStmWait)):
                wait = body.body[0]
                body = body.body[1:]
            else:
                wait = None

            if wait is None:
                assert self.top_stm is proc
                assert isinstance(body, HdlStmBlock), body
                body = body.body
                wait = body[-1]
                assert isinstance(wait, HdlStmWait), wait
                assert len(wait.val) == 0
                body = body[:-1]
                w("@instance\n")
                w(f"def instance_{self.state_counter[2]}():\n")
                with Indent(self.out):
                    w('yield delay(0)\n')
                self.state_counter[2] += 1
            else:
                pass
                # if self.top_stm is proc:
                #     w("always ")
                # w("#")
                # assert len(wait.val) == 1
                # self.visit_iHdlExpr(wait.val[0])
            _body = HdlStmBlock()
            _body.body = body
            body = _body
        else:
            tr = proc.trigger_constrain
            judge = True
            if self.top_stm is proc:
                w("@always")
                judge = False
                # if tr is None:
                #     w("@always")
                # elif tr is HdlStmProcessTriggerConstrain.FF:
                #     w("@always")
                # elif tr is HdlStmProcessTriggerConstrain.COMB:
                #     w("@always")
                # # elif tr is HdlStmProcessTriggerConstrain.LATCH:
                # #     w("always_latch ")
                # else:
                #     raise ValueError(proc.trigger_constrain)
            if tr is None:
                if sens[0] is HdlAll:
                    self.visit_iHdlExpr(sens[0])
                    w('\n')
                    if not judge:
                        w(f'def comb_{self.state_counter[0]}():')
                        self.state_counter[0] += 1
                else:
                    if judge:
                        w("yield ")
                    else:
                        w('(')
                    for last, item in iter_with_last(sens):
                        self.visit_iHdlExpr(item)
                        if not last:
                            w(", ")
                    if not judge:
                        w(")")
                        w('\n')
                        w('def seq_{}():'.format(self.state_counter[1]))
                        self.state_counter[1] += 1
            else:
                assert not sens

        # to prevent useless newline for empty always/time waits
        if skip_body:
            return True
        else:
            return self.visit_iHdlStatement_in_statement(body)

    def visit_iHdlStatement_in_statement(self, stm):
        """
        Print statement which is body of other statement
        e.g. body of process, branch of if-then-else or case of case stememnt
        """
        w = self.out.write
        if isinstance(stm, HdlStmBlock):
            if len(stm.body) == 1 and not stm.labels:
                stm = stm.body[0]
            else:
                w(" ")
                return self.visit_HdlStmBlock(stm)

        w("\n")
        with Indent(self.out):
            return self.visit_iHdlStatement(stm)

    def visit_HdlStmBlock(self, o):
        """
        :type o: HdlStmBlock
        """
        self.visit_doc(o)
        w = self.out.write
        # if o.in_preproc:
        #     w("generate ")

        # w("begin")
        # if o.labels:
        #     w(": ")
        #     w(o.labels[0])
        w("\n")
        with Indent(self.out):
            if o.body == []:
                w('pass\n')
            else:
                for s in o.body:
                    need_semi = self.visit_iHdlStatement(s)
                    # if need_semi:
                    #     w(";\n")
                    # else:
                    w("\n")
        # w("end")
        # if o.in_preproc:
        #     w(" endgenerate")
        return False

    def visit_HdlStmIf(self, o):
        """
        :type o: HdlStmIf
        """
        self.visit_doc(o)
        w = self.out.write
        # if o.in_preproc:
        #     w("generate ")
        w("if ")
        self.visit_iHdlExpr(o.cond)
        w(":")
        need_semi = self.visit_iHdlStatement_in_statement(o.if_true)

        for cond, stms in o.elifs:
            w("\n")
            w("elif ")
            self.visit_iHdlExpr(cond)
            w(":")
            need_semi = self.visit_iHdlStatement_in_statement(stms)

        ifFalse = o.if_false
        if ifFalse is not None:

            w("\n")
            w("else:")
            need_semi = self.visit_iHdlStatement_in_statement(ifFalse)

        if o.in_preproc:
            # if need_semi:
            #     w(";\n")
            # else:
            w("\n")
            # w("endgenerate")
            return False
        else:
            return need_semi

    def visit_HdlStmAssign(self, o):
        """
        :type o: HdlStmAssign
        :return: True if requires ;\\n after end
        """
        self.visit_doc(o)
        w = self.out.write
        ts = self.top_stm

        if o.time_delay is not None:
            w("yield delay(")
            self.visit_iHdlExpr(o.time_delay)
            w(")\n")
        if o.event_delay is not None:
            w("yield ")
            # if len(o.event_delay) > 1:
            #     w("(")
            for is_last, e in iter_with_last(o.event_delay):
                self.visit_iHdlExpr(e)
                if not is_last:
                    w(", ")
            # if len(o.event_delay) > 1:
            #     w(")")
            w("\n")

        reg = self.out
        f = io.StringIO()
        self.out = f
        self.visit_iHdlExpr(o.dst)
        dst = f.getvalue()

        f.truncate(0)
        f.seek(0)
        self.visit_iHdlExpr(o.src)
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

        return True

    def visit_HdlStmCase(self, o):
        """
        :type o: HdlStmCase

        :return: True if requires ;\\n after end
        """
        self.visit_doc(o)
        w = self.out.write
        # if o.uniq_constrain is not None:
        #     w(o.uniq_constrain.name.lower())
        #     w(" ")
        cases = o.cases
        idx = 0
        for k, stms in cases:
            if idx == 0:
                w('if ')
            else:
                w('elif ')
            self.visit_iHdlExpr(o.switch_on)
            w(' == ')
            self.visit_iHdlExpr(k)
            w(":")
            self.visit_iHdlStatement_in_statement(stms)
            w('\n')
            idx += 1

        defal = o.default
        if defal is not None:
            w("else:")
            self.visit_iHdlStatement_in_statement(defal)

        # w(o.type.name.lower())
        # w("(")
        # self.visit_iHdlExpr(o.switch_on)
        # w(")\n")
        # with Indent(self.out):
        #     cases = o.cases
        #     for k, stms in cases:
        #         self.visit_iHdlExpr(k)
        #         w(":")
        #         need_semi = self.visit_iHdlStatement_in_statement(stms)
        #         # if need_semi:
        #         #     w(";\n")
        #         # else:
        #         #     w("\n")
        #     defal = o.default
        #     if defal is not None:
        #         w("default:")
        #         need_semi = self.visit_iHdlStatement_in_statement(defal)
        #         if need_semi:
        #             w(";\n")
        #         else:
        #             w("\n")
        # w("endcase")
        return False

    def visit_HdlStmWait(self, o):
        """
        :type o: HdlStmWait

        :return: True if requires ;\\n after end
        """
        self.visit_doc(o)
        w = self.out.write
        w("yield delay(")
        assert len(o.val) == 1, o.val
        self.visit_iHdlExpr(o.val[0])
        w(')')
        return True

    def visit_HdlStmFor(self, o):
        """
        :type o: HdlStmFor

        :return: True if requires ;\\n after end
        """
        self.visit_doc(o)
        w = self.out.write
        # if o.in_preproc:
        #     w("generate ")

        # w("for (")
        if isinstance(o.init, HdlStmBlock):
            init_stms = o.init.body
        else:
            init_stms = [o.init, ]

        trnt = self._type_requires_nettype
        in_in_loop_spec = self.is_in_loop_spec
        try:
            self._type_requires_nettype = False
            self.is_in_loop_spec = True
            for is_last, stm in iter_with_last(init_stms):
                self.visit_iHdlStatement(stm)
                if not is_last:
                    w("\n")
        finally:
            self.is_in_loop_spec = in_in_loop_spec
            self._type_requires_nettype = trnt
            w("\n")

        # w("; ")
        w('while ')
        self.visit_iHdlExpr(o.cond)
        w(':')
        # w("; ")
        # w(")")
        need_semi = self.visit_iHdlStatement_in_statement(o.body)
        if o.in_preproc:
            # if need_semi:
            #     w(";\n")
            # else:
            w("\n")
            with Indent(self.out):
                if isinstance(o.step, HdlStmBlock):
                    step_stms = o.step.body
                else:
                    step_stms = [o.step, ]

                for is_last, stm in iter_with_last(step_stms):
                    self.visit_iHdlStatement(stm)
                    if not is_last:
                        w("\n")
            return False
        else:
            w("\n")
            with Indent(self.out):
                if isinstance(o.step, HdlStmBlock):
                    step_stms = o.step.body
                else:
                    step_stms = [o.step, ]

                for is_last, stm in iter_with_last(step_stms):
                    self.visit_iHdlStatement(stm)
                    if not is_last:
                        w("\n")
            return need_semi

    def visit_HdlStmForIn(self, o):
        """
        :type o: HdlStmForIn
        :return: True if requires ;\\n after end
        """
        self.visit_doc(o)
        raise NotImplementedError()

    def visit_HdlStmWhile(self, o):
        """
        :type o: HdlStmWhile
        :return: True if requires ;\\n after end
        """
        self.visit_doc(o)
        w = self.out.write
        w("while ")
        self.visit_iHdlExpr(o.cond)
        w(": ")
        return self.visit_iHdlStatement(o.body)

    def visit_HdlStmRepeat(self, o):
        """
        :type o: HdlStmRepeat
        :return: True if requires ;\\n after end
        """
        self.visit_doc(o)
        w = self.out.write
        w("for i in range(")
        self.visit_iHdlExpr(o.n)
        w("):")
        return self.visit_iHdlStatement(o.body)

    def visit_HdlStmReturn(self, o):
        """
        :type o: HdlStmReturn
        """
        self.visit_doc(o)
        w = self.out.write
        w("return")
        if o.val is not None:
            w(" ")
            self.visit_iHdlExpr(o.val)
        return True

    def visit_HdlStmContinue(self, o):
        """
        :type o: HdlStmContinue
        """
        self.visit_doc(o)
        self.out.write("continue")
        return True

    def visit_HdlStmBreak(self, o):
        """
        :type o: HdlStmBreak
        """
        self.visit_doc(o)
        self.out.write("break")
        return True

    def visit_HdlStmThrow(self, o):
        """
        :type o: HdlStmThrow
        """
        raise ValueError("SystemVerilog does not have exceptions")

    # [TODO] SV only
    def visit_HdlImport(self, o):
        """
        :type o: HdlImport
        """
        self.visit_doc(o)
        w = self.out.write
        w("import ")
        package, name = o.path
        self.visit_iHdlExpr(package)
        w("::")
        self.visit_iHdlExpr(name)

        return True
