from .lexer import tokenize
from .parser import Parser
from .irgen import IRGenerator
from .styling import styled_output
from .codegen import Codegen
from .seal import add_seal, verify_seal

def compile_let(source: str, output: str = "a.out", build_exec: bool = True):
    tokens = tokenize(source)
    parser = Parser(tokens)
    ast = parser.parse()

    irgen = IRGenerator()
    ir_code = irgen.generate(ast)

    styled_output(ir_code, lang="llvm")

    if build_exec:
        cg = Codegen(ir_code, output)
        exe_path = cg.build()
        return exe_path
    else:
        return ir_code

def compile_let(source: str, output: str = "a.out", build_exec: bool = True, seal: bool = True):
    tokens = tokenize(source)
    parser = Parser(tokens)
    ast = parser.parse()

    irgen = IRGenerator()
    ir_code = irgen.generate(ast)

    styled_output(ir_code, lang="llvm")

    if build_exec:
        cg = Codegen(ir_code, output)
        exe_path = cg.build()
        if seal:
            add_seal(exe_path)
            verify_seal(exe_path)
        return exe_path
    else:
        return ir_code
