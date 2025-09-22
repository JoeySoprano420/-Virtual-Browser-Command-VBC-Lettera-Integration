import argparse
from lettera.compiler import compile_let

def run_cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help=".let file to compile/run")
    parser.add_argument("--mode", choices=["letter","cmd","web","css"], default="letter")
    parser.add_argument("--no-seal", action="store_true", help="disable SEE")
    args = parser.parse_args()

    exe_path = compile_let(open(args.file).read(), output="prog.out", build_exec=True, seal=not args.no_seal)
    print(f"[Built] {exe_path}")

