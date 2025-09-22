from rich.console import Console
from rich.syntax import Syntax

console = Console()

def styled_output(code: str, lang="lettera"):
    syntax = Syntax(code, lang, theme="monokai", line_numbers=True)
    console.print(syntax)
