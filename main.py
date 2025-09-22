import sys
from lettera.compiler import compile_let

def run_file(path):
    with open(path) as f:
        source = f.read()
    ir_code = compile_let(source)
    print("\n[LLVM IR Generated]\n")
    print(ir_code)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py file.let")
    else:
        run_file(sys.argv[1])
