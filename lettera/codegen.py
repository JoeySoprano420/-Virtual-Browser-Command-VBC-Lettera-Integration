import subprocess
import os
import platform
import tempfile

class Codegen:
    def __init__(self, ir_code: str, output: str = "a.out"):
        self.ir_code = ir_code
        self.output = output
        self.system = platform.system().lower()

    def run_cmd(self, cmd):
        print("[CMD]", " ".join(cmd))
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print("[ERROR]", result.stderr)
            raise RuntimeError(f"Command failed: {' '.join(cmd)}")
        return result.stdout

    def build(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            ir_file = os.path.join(tmpdir, "prog.ll")
            asm_file = os.path.join(tmpdir, "prog.s")
            obj_file = os.path.join(tmpdir, "prog.o")

            # Write IR to file
            with open(ir_file, "w") as f:
                f.write(self.ir_code)

            # LLVM → ASM
            self.run_cmd(["llc", "-filetype=asm", "-o", asm_file, ir_file])

            # NASM / system assembler
            if self.system == "windows":
                # Use nasm + gcc for PE/COFF
                self.run_cmd(["nasm", "-f", "win64", asm_file, "-o", obj_file])
                self.run_cmd(["gcc", obj_file, "-o", self.output])
            elif self.system == "darwin":
                # macOS: use clang to assemble and link
                self.run_cmd(["clang", asm_file, "-o", self.output])
            else:
                # Linux: use gcc to assemble and link
                self.run_cmd(["gcc", asm_file, "-o", self.output])

            print(f"[SUCCESS] Built executable: {self.output}")
            return self.output
