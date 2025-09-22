import sys
from lettera.compiler import compile_let
import subprocess

def run_file(path):
    output = "a.exe" if sys.platform.startswith("win") else "a.out"
    exe_path = compile_let(open(path).read(), output=output, build_exec=True)

    print(f"\n[Executable Built] {exe_path}\n")

    # Optionally run the binary
    result = subprocess.run([f"./{exe_path}"], capture_output=True, text=True, shell=True)
    print("[Program Output]:")
    print(result.stdout)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py file.let")
    else:
        run_file(sys.argv[1])
