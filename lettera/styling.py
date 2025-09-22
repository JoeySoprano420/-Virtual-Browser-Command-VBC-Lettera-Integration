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

def render_ui(ast):
    html_snippets = []
    for node in ast.children:
        if node.type == "UIElement":
            html_snippets.append(generate_ui(node))
    html_doc = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Georgia, serif; margin: 20px; background: #f8f0e3; }}
            button {{ background: violet; color: white; padding: 10px; margin: 5px; border: none; cursor: pointer; }}
            form {{ margin-top: 15px; }}
            div {{ margin: 10px; font-size: 18px; }}
        </style>
    </head>
    <body>
        {"".join(html_snippets)}
    </body>
    </html>
    """
    return html_doc

def generate_ui(node):
    if node.value == "Form":
        fields = "".join([
            f'<label>{c.value}: <input id="{c.value}" oninput="updateVar(\'{c.value}\', this.value)"/></label><br>'
            for c in node.children if c.type == "UIField"
        ])
        return f"""
        <form onsubmit="event.preventDefault(); runSubmit();">
            {fields}
            <button type="submit">Submit</button>
        </form>
        """
    elif node.value == "Output":
        msg = next((c.value.strip('"') for c in node.children if c.type == "UIShow"), "")
        return f'<div id="output">{msg}</div>'

def render_ui(ast):
    html_snippets = []
    for node in ast.children:
        if node.type == "UIElement":
            html_snippets.append(generate_ui(node))
    html_doc = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Georgia, serif; margin: 20px; background: #f8f0e3; }}
            button {{ background: violet; color: white; padding: 10px; margin: 5px; border: none; cursor: pointer; }}
            div {{ margin: 10px; font-size: 18px; }}
        </style>
        <script>
            let vars = {{}};
            function updateVar(name, value) {{
                vars[name] = value;
                if(document.getElementById("output")) {{
                    document.getElementById("output").innerText = "Hello, " + (vars["Name"] || "Guest");
                }}
            }}
            function runSubmit() {{
                alert("Welcome, " + (vars["Name"] || "Guest"));
            }}
        </script>
    </head>
    <body>
        {"".join(html_snippets)}
    </body>
    </html>
    """
    return html_doc

def generate_ui(node):
    if node.value == "Button":
        label = next((c.value.strip('"') for c in node.children if c.type == "UILabel"), "Button")
        action = next((c.value.strip('"') for c in node.children if c.type == "UIAction"), "")
        return f'<button onclick="alert(\'{action}\')">{label}</button>'
    elif node.value == "Form":
        fields = "".join([f'<label>{c.value}: <input name="{c.value}"/></label><br>' for c in node.children if c.type == "UIField"])
        return f"""
        <form onsubmit="alert('Form submitted'); return false;">
            {fields}
            <button type="submit">Submit</button>
        </form>
        """
    elif node.value == "Output":
        msg = next((c.value.strip('"') for c in node.children if c.type == "UIShow"), "")
        return f'<div>{msg}</div>'

elif self.peek()[0] == "IDENT" and self.peek()[1] == "Field:":
    self.eat("IDENT")
    val = self.eat("IDENT")[1]
    children.append(ASTNode("UIField", value=val))
elif self.peek()[0] == "IDENT" and self.peek()[1] == "Show:":
    self.eat("IDENT")
    val = self.eat("STRING")[1]
    children.append(ASTNode("UIShow", value=val))

