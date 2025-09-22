from .lexer import tokenize
from .parser import Parser
from .irgen import IRGenerator
from .styling import styled_output

def compile_let(source: str):
    tokens = tokenize(source)
    parser = Parser(tokens)
    ast = parser.parse()

    irgen = IRGenerator()
    ir_code = irgen.generate(ast)

    styled_output(ir_code, lang="llvm")
    return ir_code
