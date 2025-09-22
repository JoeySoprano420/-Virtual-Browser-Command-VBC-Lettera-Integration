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

def parse_repeat(self):
    self.eat("IDENT")  # Repeat
    times = int(self.eat("NUMBER")[1])
    self.eat("IDENT")  # "Times:"
    block = self.parse_block()
    return ASTNode("Repeat", value=times, children=[block])

def parse_while(self):
    self.eat("IDENT")  # While
    left = self.eat("IDENT")[1]
    op = self.eat("IDENT")[1]
    right = self.eat("NUMBER")[1]
    block = self.parse_block()
    return ASTNode("While", value=(left, op, int(right)), children=[block])

def parse_for(self):
    self.eat("IDENT")  # For
    var = self.eat("IDENT")[1]
    self.eat("IDENT")  # '='
    start = int(self.eat("NUMBER")[1])
    self.eat("IDENT")  # 'to'
    end = int(self.eat("NUMBER")[1])
    block = self.parse_block()
    return ASTNode("For", value=(var, start, end), children=[block])

def parse_ui_list(self):
    self.eat("IDENT")  # "UI"
    self.eat("IDENT")  # "List:"
    self.eat("IDENT")  # "For"
    var = self.eat("IDENT")[1]
    self.eat("IDENT")  # "in"
    arr = self.eat("IDENT")[1]
    block = self.parse_block()
    return ASTNode("UIList", value=(var, arr), children=[block])

def parse_onmessage(self):
    self.eat("IDENT")  # "OnMessage"
    msg_type = self.eat("STRING")[1]
    block = self.parse_block()
    return ASTNode("OnMessage", value=msg_type, children=[block])

    def run(self):
        while True:
            msg = self.q.get()
            if msg == "STOP": break
            self.handle_message(msg)

    def handle_message(self, msg):
        # parse structured msg
        typ, payload = msg.get("type"), msg.get("data")
        if typ in self.vars.get("listeners", {}):
            # update bound variable
            self.vars["Tasks"].append(payload)
            self.update_ui()
        print(f"[{self.path}] handled message {typ} → {payload}")

    def send(self, msg):
        self.q.put(msg)

def update_ui(self):
    # Emit JS refresh in Web Mode
    if self.vars.get("WebMode"):
        html = "".join(generate_ui(node) for node in self.vars.get("UI", []))
        js = f"""
        <script>
        document.getElementById("vbc-ui").innerHTML = `{html}`;
        </script>
        """
        self.vars["Output"].append(js)


def parse_expression(self):
    if self.peek()[0] == "NUMBER":
        return ASTNode("Number", value=int(self.eat("NUMBER")[1]))
    elif self.peek()[0] == "STRING":
        return ASTNode("String", value=self.eat("STRING")[1].strip('"'))
    elif self.peek()[0] == "IDENT" and self.peek()[1] == "[":
        return self.parse_array()
    elif self.peek()[0] == "IDENT" and self.peek()[1] == "{":
        return self.parse_struct()
    elif self.peek()[0] == "IDENT":
        return ASTNode("Var", value=self.eat("IDENT")[1])
    else:
        raise RuntimeError("Unexpected expression")

def parse_array(self):
    self.eat("IDENT")  # '['
    elements = []
    while self.peek()[1] != "]":
        elements.append(self.parse_expression())
        if self.peek()[1] == ",":
            self.eat("IDENT")
    self.eat("IDENT")  # ']'
    return ASTNode("Array", children=elements)

def parse_struct(self):
    self.eat("IDENT")  # '{'
    fields = []
    while self.peek()[1] != "}":
        key = self.eat("IDENT")[1]
        self.eat("IDENT")  # '='
        val = self.parse_expression()
        fields.append(ASTNode("Field", value=key, children=[val]))
        if self.peek()[1] == ",":
            self.eat("IDENT")
    self.eat("IDENT")  # '}'
    return ASTNode("Struct", children=fields)

def parse_channel(self):
    self.eat("IDENT")  # Channel
    name = self.eat("IDENT")[1]
    return ASTNode("Channel", value=name)

def parse_spawn(self):
    self.eat("IDENT")  # Spawn
    name = self.eat("IDENT")[1]
    self.eat("IDENT")  # '('
    self.eat("IDENT")  # ')'
    block = self.parse_block()
    return ASTNode("Spawn", value=name, children=[block])

def parse_send(self):
    self.eat("IDENT")  # Send
    ch = self.eat("IDENT")[1]
    self.eat("IDENT")  # "with"
    val = self.parse_expression()
    return ASTNode("Send", value=ch, children=[val])

def parse_receive(self):
    self.eat("IDENT")  # Receive
    ch = self.eat("IDENT")[1]
    return ASTNode("Receive", value=ch)

def parse_ui_dropdown(self):
    self.eat("IDENT")  # UI
    self.eat("IDENT")  # Dropdown:
    options = self.eat("IDENT")[1]  # Options var
    self.eat("IDENT")  # Bind:
    bind = self.eat("IDENT")[1]
    return ASTNode("UIDropdown", value=(options, bind))

def parse_ui_table(self):
    self.eat("IDENT")  # UI
    self.eat("IDENT")  # Table:
    cols = self.parse_array()
    self.eat("IDENT")  # Data:
    data = self.eat("IDENT")[1]
    return ASTNode("UITable", value=(cols, data))

def parse_ui_chart(self):
    self.eat("IDENT")  # UI
    self.eat("IDENT")  # Chart:
    typ = self.eat("IDENT")[1]
    self.eat("IDENT")  # Data:
    data = self.eat("IDENT")[1]
    return ASTNode("UIChart", value=(typ, data))

