from .lexer import CompileError

def analyze(ast):
    symbols = {}
    def visit_expr(node):
        kind = node["type"]
        if kind == "Literal":
            return node["valueType"]
        if kind == "Identifier":
            name = node["name"]
            if name not in symbols:
                raise CompileError(f"Variabel '{name}' belum dideklarasikan.", node.get("line", 1), 1, "Semantic")
            return symbols[name]["type"]
        if kind == "UnaryExpression":
            t = visit_expr(node["argument"])
            if t != "number":
                raise CompileError("Operator unary hanya dapat digunakan pada angka.", 1, 1, "Semantic")
            return "number"
        if kind == "BinaryExpression":
            left, right = visit_expr(node["left"]), visit_expr(node["right"])
            op = node["operator"]
            if op == "+" and left == right == "string":
                return "string"
            if left != "number" or right != "number":
                raise CompileError(f"Operator '{op}' membutuhkan operand angka (kecuali penggabungan teks dengan +).", 1, 1, "Semantic")
            return "number"
        return "unknown"

    for stmt in ast["body"]:
        if stmt["type"] == "LetDeclaration":
            name = stmt["name"]
            if name in symbols:
                raise CompileError(f"Variabel '{name}' sudah dideklarasikan.", stmt.get("line", 1), 1, "Semantic")
            value_type = visit_expr(stmt["value"])
            symbols[name] = {"type": value_type, "value": None}
        else:
            visit_expr(stmt["value"])
    return symbols
