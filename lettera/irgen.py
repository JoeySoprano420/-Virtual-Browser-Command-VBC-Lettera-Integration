from llvmlite import ir

class IRGenerator:
    def __init__(self):
        self.module = ir.Module(name="lettera_module")
        self.printf = None

    def declare_printf(self):
        if not self.printf:
            voidptr_ty = ir.IntType(8).as_pointer()
            fnty = ir.FunctionType(ir.IntType(32), [voidptr_ty], var_arg=True)
            self.printf = ir.Function(self.module, fnty, name="printf")
        return self.printf

    def generate(self, ast):
        main_ty = ir.FunctionType(ir.IntType(32), [])
        main_func = ir.Function(self.module, main_ty, name="main")
        block = main_func.append_basic_block(name="entry")
        builder = ir.IRBuilder(block)

        printf = self.declare_printf()

        for node in ast.children:
            if node.type == "Block":
                for child in node.children:
                    if child.type in ("AbovePrint", "BelowPrint"):
                        msg = child.value.strip('"') + "\n"
                        c_fmt = ir.Constant(ir.ArrayType(ir.IntType(8), len(msg)),
                                            bytearray(msg.encode("utf8")))
                        global_fmt = ir.GlobalVariable(self.module, c_fmt.type, name="str")
                        global_fmt.linkage = 'internal'
                        global_fmt.global_constant = True
                        global_fmt.initializer = c_fmt
                        fmt_ptr = builder.bitcast(global_fmt, ir.IntType(8).as_pointer())
                        builder.call(printf, [fmt_ptr])

        builder.ret(ir.Constant(ir.IntType(32), 0))
        return str(self.module)

class IRGenerator:
    def __init__(self):
        self.module = ir.Module(name="lettera_module")
        self.printf = None
        self.symbols = {}

    def declare_printf(self):
        if not self.printf:
            voidptr_ty = ir.IntType(8).as_pointer()
            fnty = ir.FunctionType(ir.IntType(32), [voidptr_ty], var_arg=True)
            self.printf = ir.Function(self.module, fnty, name="printf")
        return self.printf

    def eval_expr(self, builder, node):
        if node.type == "Number":
            return ir.Constant(ir.IntType(32), node.value)
        elif node.type == "Var":
            return builder.load(self.symbols[node.value])
        elif node.type == "Add":
            left_name = node.value
            right_node = node.children[0]
            left = builder.load(self.symbols[left_name])
            right = self.eval_expr(builder, right_node)
            return builder.add(left, right, name="addtmp")
        else:
            raise RuntimeError(f"Unknown expr: {node}")

    def generate(self, ast):
        main_ty = ir.FunctionType(ir.IntType(32), [])
        main_func = ir.Function(self.module, main_ty, name="main")
        block = main_func.append_basic_block(name="entry")
        builder = ir.IRBuilder(block)

        printf = self.declare_printf()

        for node in ast.children:
            if node.type == "Block":
                for child in node.children:
                    if child.type == "Equation":
                        name = child.value
                        val = self.eval_expr(builder, child.children[0])
                        var = builder.alloca(ir.IntType(32), name=name)
                        builder.store(val, var)
                        self.symbols[name] = var
                    elif child.type in ("AbovePrint", "BelowPrint"):
                        msg = child.value.strip('"') + "\n"
                        c_fmt = ir.Constant(ir.ArrayType(ir.IntType(8), len(msg)),
                                            bytearray(msg.encode("utf8")))
                        global_fmt = ir.GlobalVariable(self.module, c_fmt.type, name=f"str{len(msg)}")
                        global_fmt.linkage = 'internal'
                        global_fmt.global_constant = True
                        global_fmt.initializer = c_fmt
                        fmt_ptr = builder.bitcast(global_fmt, ir.IntType(8).as_pointer())
                        builder.call(printf, [fmt_ptr])
        builder.ret(ir.Constant(ir.IntType(32), 0))
        return str(self.module)

def generate_function(self, node):
    name = node.value
    args = [ir.IntType(32) for _ in node.children[0].children]
    fnty = ir.FunctionType(ir.IntType(32), args)
    func = ir.Function(self.module, fnty, name=name)

    block = func.append_basic_block(name="entry")
    builder = ir.IRBuilder(block)

    # map args
    for idx, arg in enumerate(func.args):
        var = builder.alloca(ir.IntType(32), name=node.children[0].children[idx])
        builder.store(arg, var)
        self.symbols[node.children[0].children[idx]] = var

    # compile body
    for child in node.children[1].children:
        if child.type == "Equation":
            name = child.value
            val = self.eval_expr(builder, child.children[0])
            var = builder.alloca(ir.IntType(32), name=name)
            builder.store(val, var)
            self.symbols[name] = var
    ret_val = self.eval_expr(builder, node.children[2])
    builder.ret(ret_val)

def generate_if(self, builder, node):
    left, op, right = node.value
    lval = builder.load(self.symbols[left])
    rval = builder.load(self.symbols[right])
    cond = builder.icmp_signed(op, lval, rval)

    then_block = builder.function.append_basic_block("then")
    else_block = builder.function.append_basic_block("else")
    merge_block = builder.function.append_basic_block("ifcont")

    builder.cbranch(cond, then_block, else_block)

    builder.position_at_end(then_block)
    for child in node.children[0].children:
        self.emit_statement(builder, child)
    builder.branch(merge_block)

    builder.position_at_end(else_block)
    if node.children[1]:
        for child in node.children[1].children:
            self.emit_statement(builder, child)
    builder.branch(merge_block)

    builder.position_at_end(merge_block)

