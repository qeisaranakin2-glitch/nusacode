import re
from dataclasses import dataclass

@dataclass
class Token:
    type: str
    value: object
    line: int
    column: int

    def as_dict(self):
        return {"type": self.type, "value": self.value, "line": self.line, "column": self.column}

class CompileError(Exception):
    def __init__(self, message, line=1, column=1, stage="Lexer"):
        super().__init__(message)
        self.message, self.line, self.column, self.stage = message, line, column, stage

TOKEN_RE = re.compile(
    r'(?P<SPACE>[ \t\r]+)|(?P<NEWLINE>\n)|'
    r'(?P<COMMENT>\#.*)|'
    r'(?P<STRING>"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\')|'
    r'(?P<NUMBER>\d+(?:\.\d+)?)|'
    r'(?P<IDENT>[A-Za-z_][A-Za-z0-9_]*)|'
    r'(?P<OP>[=+\-*/();])'
)

def tokenize(source):
    tokens, pos, line, col = [], 0, 1, 1
    while pos < len(source):
        match = TOKEN_RE.match(source, pos)
        if not match:
            raise CompileError(f"Karakter tidak dikenal: {source[pos]!r}", line, col)
        kind, raw = match.lastgroup, match.group()
        if kind == "NEWLINE":
            line, col = line + 1, 1
        elif kind in ("SPACE", "COMMENT"):
            col += len(raw)
        else:
            if kind == "IDENT":
                upper = raw.upper()
                if upper in ("LET", "PRINT"):
                    kind, value = upper, upper
                else:
                    kind, value = "IDENT", raw
            elif kind == "NUMBER":
                value = float(raw) if "." in raw else int(raw)
            elif kind == "STRING":
                # Decode common escaped characters without evaluating Python expressions.
                body = raw[1:-1]
                value = bytes(body, "utf-8").decode("unicode_escape")
            else:
                kind, value = raw, raw
            tokens.append(Token(kind, value, line, col))
            col += len(raw)
        pos = match.end()
    tokens.append(Token("EOF", None, line, col))
    return tokens
