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
