import json

def serialize(node):
    if node.type == "Number": return node.value
    if node.type == "String": return node.value
    if node.type == "Array": return [serialize(c) for c in node.children]
    if node.type == "Struct": return {f.value: serialize(f.children[0]) for f in node.children}
    return str(node.value)

def deserialize(data):
    return data  # JSON already structured
