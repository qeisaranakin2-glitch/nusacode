from .lexer import CompileError

def execute(ast):
    environment, output = {}, []
    def evaluate(node):
        kind = node["type"]
        if kind == "Literal":
            return node["value"]
        if kind == "Identifier":
            return environment[node["name"]]
        if kind == "UnaryExpression":
            value = evaluate(node["argument"])
            return value if node["operator"] == "+" else -value
        if kind == "BinaryExpression":
            left, right = evaluate(node["left"]), evaluate(node["right"])
            op = node["operator"]
            if op == "+": return left + right
            if op == "-": return left - right
            if op == "*": return left * right
            if op == "/":
                if right == 0:
                    raise CompileError("Tidak bisa membagi dengan nol.", 1, 1, "Runtime")
                return left / right
        raise CompileError("Node AST tidak dikenali.", 1, 1, "Runtime")

    for stmt in ast["body"]:
        if stmt["type"] == "LetDeclaration":
            environment[stmt["name"]] = evaluate(stmt["value"])
        elif stmt["type"] == "PrintStatement":
            output.append(str(evaluate(stmt["value"])))
    return output, environment
