from .lexer import CompileError

class Parser:
    def __init__(self, tokens):
        self.tokens, self.current = tokens, 0

    def peek(self):
        return self.tokens[self.current]

    def advance(self):
        token = self.peek()
        if token.type != "EOF":
            self.current += 1
        return token

    def match(self, *types):
        if self.peek().type in types:
            return self.advance()
        return None

    def expect(self, kind, message=None):
        token = self.match(kind)
        if token:
            return token
        here = self.peek()
        raise CompileError(message or f"Seharusnya '{kind}', ditemukan {here.type}.",
                           here.line, here.column, "Parser")

    def parse(self):
        statements = []
        while self.peek().type != "EOF":
            statements.append(self.statement())
        return {"type": "Program", "body": statements}

    def statement(self):
        if self.match("LET"):
            name = self.expect("IDENT", "Setelah LET harus ada nama variabel.")
            self.expect("=", "Deklarasi variabel harus menggunakan '='.")
            value = self.expression()
            self.expect(";", "Akhiri deklarasi LET dengan ';'.")
            return {"type": "LetDeclaration", "name": name.value, "value": value, "line": name.line}
        if self.match("PRINT"):
            token = self.tokens[self.current - 1]
            value = self.expression()
            self.expect(";", "Akhiri perintah PRINT dengan ';'.")
            return {"type": "PrintStatement", "value": value, "line": token.line}
        here = self.peek()
        raise CompileError("Pernyataan harus dimulai dengan LET atau PRINT.", here.line, here.column, "Parser")

    def expression(self):
        node = self.term()
        while self.peek().type in ("+", "-"):
            op = self.advance().type
            node = {"type": "BinaryExpression", "operator": op, "left": node, "right": self.term()}
        return node

    def term(self):
        node = self.unary()
        while self.peek().type in ("*", "/"):
            op = self.advance().type
            node = {"type": "BinaryExpression", "operator": op, "left": node, "right": self.unary()}
        return node

    def unary(self):
        if self.peek().type in ("+", "-"):
            op = self.advance().type
            return {"type": "UnaryExpression", "operator": op, "argument": self.unary()}
        return self.primary()

    def primary(self):
        token = self.match("NUMBER", "STRING")
        if token:
            return {"type": "Literal", "value": token.value, "valueType": "number" if token.type == "NUMBER" else "string"}
        token = self.match("IDENT")
        if token:
            return {"type": "Identifier", "name": token.value, "line": token.line}
        if self.match("("):
            expr = self.expression()
            self.expect(")", "Kurung tutup ')' belum ditemukan.")
            return expr
        here = self.peek()
        raise CompileError("Ekspresi tidak valid. Periksa angka, teks, variabel, atau tanda kurung.",
                           here.line, here.column, "Parser")
