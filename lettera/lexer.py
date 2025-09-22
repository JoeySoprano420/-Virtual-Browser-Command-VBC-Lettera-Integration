import re

TOKEN_SPEC = [
    ("MODULE", r"Module:"),
    ("ENTRY", r"Entry:"),
    ("FUNC", r"Func"),
    ("BLOCK", r"Block:"),
    ("EQUATION", r"Equation:"),
    ("ABOVE", r"Above:"),
    ("BELOW", r"Below:"),
    ("END", r"End:"),
    ("RETURN", r"Return"),
    ("IDENT", r"[A-Za-z_][A-Za-z0-9_]*"),
    ("STRING", r"\".*?\""),
    ("NUMBER", r"\d+"),
    ("NEWLINE", r"\n"),
    ("SKIP", r"[ \t]+"),
    ("MISMATCH", r"."),
]

master_pat = re.compile("|".join(f"(?P<{name}>{pattern})" for name, pattern in TOKEN_SPEC))

def tokenize(code):
    tokens = []
    for mo in master_pat.finditer(code):
        kind = mo.lastgroup
        value = mo.group()
        if kind == "SKIP" or kind == "NEWLINE":
            continue
        elif kind == "MISMATCH":
            raise RuntimeError(f"Unexpected character: {value}")
        else:
            tokens.append((kind, value))
    return tokens
