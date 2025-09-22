from .ast import ASTNode

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else (None, None)

    def eat(self, kind=None):
        token = self.peek()
        if kind and token[0] != kind:
            raise RuntimeError(f"Expected {kind}, got {token}")
        self.pos += 1
        return token

    def parse(self):
        nodes = []
        while self.peek()[0]:
            if self.peek()[0] == "MODULE":
                nodes.append(self.parse_module())
            elif self.peek()[0] == "ENTRY":
                nodes.append(self.parse_entry())
            elif self.peek()[0] == "BLOCK":
                nodes.append(self.parse_block())
            elif self.peek()[0] == "END":
                nodes.append(self.parse_end())
            else:
                self.eat()  # skip unrecognized for now
        return ASTNode("Program", children=nodes)

    def parse_module(self):
        self.eat("MODULE")
        return ASTNode("Module")

    def parse_entry(self):
        self.eat("ENTRY")
        self.eat("FUNC")
        name = self.eat("IDENT")[1]
        return ASTNode("EntryFunc", value=name)

    def parse_block(self):
        self.eat("BLOCK")
        children = []
        while self.peek()[0] not in ("END", None):
            if self.peek()[0] == "EQUATION":
                self.eat("EQUATION")
                ident = self.eat("IDENT")[1]
                self.eat("IDENT")  # '='
                val = self.eat("IDENT")[1]
                children.append(ASTNode("Equation", value=(ident, val)))
            elif self.peek()[0] == "ABOVE":
                self.eat("ABOVE")
                msg = self.eat("STRING")[1]
                children.append(ASTNode("AbovePrint", value=msg))
            elif self.peek()[0] == "BELOW":
                self.eat("BELOW")
                msg = self.eat("STRING")[1]
                children.append(ASTNode("BelowPrint", value=msg))
            else:
                self.eat()
        return ASTNode("Block", children=children)

    def parse_end(self):
        self.eat("END")
        self.eat("RETURN")
        val = self.eat("NUMBER")[1]
        return ASTNode("Return", value=int(val))

def parse_block(self):
    self.eat("BLOCK")
    children = []
    while self.peek()[0] not in ("END", None):
        if self.peek()[0] == "EQUATION":
            self.eat("EQUATION")
            ident = self.eat("IDENT")[1]
            self.eat("IDENT")  # '='
            expr = self.parse_expression()
            children.append(ASTNode("Equation", value=ident, children=[expr]))
        elif self.peek()[0] == "ABOVE":
            self.eat("ABOVE")
            msg = self.eat("STRING")[1]
            children.append(ASTNode("AbovePrint", value=msg))
        elif self.peek()[0] == "BELOW":
            self.eat("BELOW")
            msg = self.eat("STRING")[1]
            children.append(ASTNode("BelowPrint", value=msg))
        else:
            self.eat()
    return ASTNode("Block", children=children)

def parse_expression(self):
    # Simple expression parser: supports X + Y and numbers
    if self.peek()[0] == "NUMBER":
        val = int(self.eat("NUMBER")[1])
        return ASTNode("Number", value=val)
    elif self.peek()[0] == "IDENT":
        val = self.eat("IDENT")[1]
        if self.peek()[1] == "+":
            self.eat("IDENT")  # eat '+'
            right = self.parse_expression()
            return ASTNode("Add", value=val, children=[right])
        else:
            return ASTNode("Var", value=val)
    else:
        raise RuntimeError("Unexpected expression")

def parse_func(self):
    self.eat("FUNC")
    name = self.eat("IDENT")[1]
    self.eat("IDENT")  # '('
    args = []
    while self.peek()[0] != "IDENT" or self.peek()[1] != ")":
        if self.peek()[0] == "IDENT":
            args.append(self.eat("IDENT")[1])
        else:
            self.eat()
    self.eat("IDENT")  # ')'
    block = self.parse_block()
    end = self.parse_end()
    return ASTNode("Function", value=name, children=[ASTNode("Args", children=args), block, end])

def parse_if(self):
    self.eat("IDENT")  # "If"
    left = self.eat("IDENT")[1]
    op = self.eat("IDENT")[1]  # '>', '<', '=='
    right = self.eat("IDENT")[1]
    then_block = self.parse_block()
    else_block = None
    if self.peek()[1] == "Else:":
        self.eat("IDENT")
        else_block = self.parse_block()
    return ASTNode("If", value=(left, op, right), children=[then_block, else_block])

def parse_ui(self):
    kind = self.eat("IDENT")[1]  # "UI"
    element = self.eat("IDENT")[1]  # Button/Form/Output
    children = []

    while self.peek()[0] not in ("END", "BLOCK", None):
        if self.peek()[0] == "IDENT" and self.peek()[1] == "Label:":
            self.eat("IDENT")
            val = self.eat("STRING")[1]
            children.append(ASTNode("UILabel", value=val))
        elif self.peek()[0] == "IDENT" and self.peek()[1] == "Action:":
            self.eat("IDENT")
            val = self.eat("STRING")[1]
            children.append(ASTNode("UIAction", value=val))
        elif self.peek()[0] == "IDENT" and self.peek()[1] == "Field:":
            self.eat("IDENT")
            val = self.eat("IDENT")[1]
            children.append(ASTNode("UIField", value=val))
        elif self.peek()[0] == "IDENT" and self.peek()[1] == "Show:":
            self.eat("IDENT")
            val = self.eat("STRING")[1]
            children.append(ASTNode("UIShow", value=val))
        elif self.peek()[0] == "IDENT" and self.peek()[1] == "Submit:":
            self.eat("IDENT")
            children.append(ASTNode("UISubmit"))
        else:
            break

    return ASTNode("UIElement", value=element, children=children)

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

