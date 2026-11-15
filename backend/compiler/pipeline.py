from .lexer import tokenize, CompileError
from .parser import Parser
from .semantic import analyze
from .interpreter import execute
from .ir import generate_ir

def compile_source(source):
    try:
        tokens = tokenize(source)
        ast = Parser(tokens).parse()
        symbols = analyze(ast)
        ir = generate_ir(ast)
        output, values = execute(ast)
        symbol_table = [
            {"name": name, "type": info["type"], "value": values.get(name)}
            for name, info in symbols.items()
        ]
        return {
            "success": True,
            "tokens": [t.as_dict() for t in tokens if t.type != "EOF"],
            "ast": ast,
            "symbolTable": symbol_table,
            "intermediateCode": ir,
            "output": output,
            "error": None
        }
    except CompileError as exc:
        return {
            "success": False, "tokens": [], "ast": None, "symbolTable": [],
            "intermediateCode": [], "output": [],
            "error": {"stage": exc.stage, "message": exc.message, "line": exc.line, "column": exc.column}
        }
