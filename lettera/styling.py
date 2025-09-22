from rich.console import Console
from rich.syntax import Syntax
import webbrowser, tempfile

console = Console()

def styled_output(code: str, mode="letter", lang="llvm"):
    if mode == "letter":
        syntax = Syntax(code, lang, theme="monokai", line_numbers=True)
        console.print("[bold violet]--- Letter Script Mode ---[/bold violet]")
        console.print(syntax)
    elif mode == "cmd":
        console.print(f"[green on black]{code}[/green on black]")
    elif mode == "web":
        html = f"<html><body><pre>{code}</pre></body></html>"
        path = tempfile.mktemp(suffix=".html")
        with open(path, "w") as f:
            f.write(html)
        webbrowser.open(f"file://{path}")
    elif mode == "css":
        css_template = f"<style>pre {{ color: violet; background: black; }}</style>"
        html = f"<html><head>{css_template}</head><body><pre>{code}</pre></body></html>"
        path = tempfile.mktemp(suffix=".html")
        with open(path, "w") as f:
            f.write(html)
        webbrowser.open(f"file://{path}")

