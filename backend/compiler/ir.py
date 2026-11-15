def generate_ir(ast):
    instructions, temp = [], 0
    def expr(node):
        nonlocal temp
        kind = node["type"]
        if kind == "Literal":
            return repr(node["value"])
        if kind == "Identifier":
            return node["name"]
        if kind == "UnaryExpression":
            value = expr(node["argument"])
            temp += 1
            name = f"t{temp}"
            instructions.append(f"{name} = {node['operator']}{value}")
            return name
        if kind == "BinaryExpression":
            left, right = expr(node["left"]), expr(node["right"])
            temp += 1
            name = f"t{temp}"
            instructions.append(f"{name} = {left} {node['operator']} {right}")
            return name
    for stmt in ast["body"]:
        if stmt["type"] == "LetDeclaration":
            instructions.append(f"{stmt['name']} = {expr(stmt['value'])}")
        else:
            instructions.append(f"PRINT {expr(stmt['value'])}")
    return instructions
