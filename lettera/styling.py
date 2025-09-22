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

def generate_ui(node):
    if node.type == "UIDropdown":
        options, bind = node.value
        return f"""
        <select id="{bind}" onchange="vars['{bind}']=this.value;">
            <script>
                (vars['{options}']||[]).forEach(opt=>{
                    let o=document.createElement('option');
                    o.value=opt; o.text=opt;
                    document.getElementById('{bind}').appendChild(o);
                });
            </script>
        </select>
        """
    elif node.type == "UITable":
        cols, data = node.value
        cols = [c.value for c in cols.children]
        return f"""
        <table border="1">
            <tr>{"".join(f"<th>{c}</th>" for c in cols)}</tr>
            <script>
                Object.keys(vars['{data}']||{{}}).forEach(k=>{
                    let tr=document.createElement('tr');
                    tr.innerHTML = `<td>${{k}}</td><td>${{vars['{data}'][k]}}</td>`;
                    document.currentScript.parentNode.appendChild(tr);
                });
            </script>
        </table>
        """
    elif node.type == "UIChart":
        typ, data = node.value
        return f"""
        <canvas id="chart_{data}" width="400" height="200"></canvas>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <script>
            new Chart(document.getElementById("chart_{data}"), {{
                type: '{typ.lower()}',
                data: {{
                    labels: Object.keys(vars['{data}']),
                    datasets: [{{
                        label: '{data}',
                        data: Object.values(vars['{data}']),
                        backgroundColor: ['violet','gold','silver']
                    }}]
                }}
            }});
        </script>
        """

def generate_ui(node):
    if node.type == "UIList":
        var, arr = node.value
        # Render as <ul> populated via JS binding
        return f"""
        <ul id="list_{arr}"></ul>
        <script>
            if(Array.isArray(vars['{arr}'])) {{
                const ul = document.getElementById("list_{arr}");
                ul.innerHTML = "";
                vars['{arr}'].forEach(val => {{
                    let li = document.createElement("li");
                    li.textContent = val;
                    ul.appendChild(li);
                }});
            }}
        </script>
        """
    elif node.type == "If":
        cond_id = f"cond_{hash(str(node.value)) & 0xffff}"
        then_html = "".join(generate_ui(c) for c in node.children[0].children)
        else_html = "".join(generate_ui(c) for c in (node.children[1].children if node.children[1] else []))
        left, op, right = node.value
        return f"""
        <div id="{cond_id}"></div>
        <script>
            function update_cond_{cond_id}() {{
                if(vars['{left}'] {op} {right}) {{
                    document.getElementById("{cond_id}").innerHTML = `{then_html}`;
                }} else {{
                    document.getElementById("{cond_id}").innerHTML = `{else_html}`;
                }}
            }}
            update_cond_{cond_id}();
        </script>
        """

def generate_component(node):
    name = node.value
    html_id = f"comp_{name.lower()}_{hash(name) & 0xffff}"

    body_html = "".join(generate_ui(c) for c in node.children)
    return f"""
    <div id="{html_id}">
        {body_html}
    </div>
    <script>
        if(!vars['{name}']) vars['{name}'] = {{state: {{}}, setState: (k,v)=>{{ vars['{name}'].state[k]=v; render_{name}(); }}}};

        function render_{name}() {{
            document.getElementById("{html_id}").innerHTML = `{body_html}`;
        }}
        render_{name}();
    </script>
    """

