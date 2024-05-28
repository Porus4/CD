import re

# Token types
INTEGER = 'INTEGER'
PLUS = 'PLUS'
MINUS = 'MINUS'
MULTIPLY = 'MULTIPLY'
DIVIDE = 'DIVIDE'
LPAREN = 'LPAREN'
RPAREN = 'RPAREN'
EOF = 'EOF'

# Token class
class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()

# Lexer
class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0

    def error(self):
        raise Exception('Invalid character')

    def advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            return Token(EOF, None)
        return self.text[self.pos]

    def skip_whitespace(self):
        while self.pos < len(self.text) and self.text[self.pos].isspace():
            self.pos += 1

    def integer(self):
        result = ''
        while self.pos < len(self.text) and self.text[self.pos].isdigit():
            result += self.text[self.pos]
            self.pos += 1
        return int(result)

    def get_next_token(self):
        while self.pos < len(self.text):
            current_char = self.text[self.pos]

            if current_char.isspace():
                self.skip_whitespace()
                continue

            if current_char.isdigit():
                return Token(INTEGER, self.integer())

            if current_char == '+':
                self.pos += 1
                return Token(PLUS, '+')

            if current_char == '-':
                self.pos += 1
                return Token(MINUS, '-')

            if current_char == '*':
                self.pos += 1
                return Token(MULTIPLY, '*')

            if current_char == '/':
                self.pos += 1
                return Token(DIVIDE, '/')

            if current_char == '(':
                self.pos += 1
                return Token(LPAREN, '(')

            if current_char == ')':
                self.pos += 1
                return Token(RPAREN, ')')

            self.error()

        return Token(EOF, None)

# Parser
class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception('Invalid syntax')

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def factor(self):
        token = self.current_token
        if token.type == INTEGER:
            self.eat(INTEGER)
            return token.value
        elif token.type == LPAREN:
            self.eat(LPAREN)
            result = self.expr()
            self.eat(RPAREN)
            return result

    def term(self):
        result = self.factor()

        while self.current_token.type in (MULTIPLY, DIVIDE):
            token = self.current_token
            if token.type == MULTIPLY:
                self.eat(MULTIPLY)
                result *= self.factor()
            elif token.type == DIVIDE:
                self.eat(DIVIDE)
                result /= self.factor()

        return result

    def expr(self):
        result = self.term()

        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
                result += self.term()
            elif token.type == MINUS:
                self.eat(MINUS)
                result -= self.term()

        return result

# Intermediate Code Generator
class IntermediateCodeGenerator:
    def __init__(self, parser):
        self.parser = parser

    def generate(self):
        return self.parser.expr()

# Main
def main():
    while True:
        try:
            text = input('Enter exp')
        except EOFError:
            break
        if not text:
            continue

        lexer = Lexer(text)
        parser = Parser(lexer)
        print(lexer)
        inter_code_gen = IntermediateCodeGenerator(parser)
        result = inter_code_gen.generate()
        print(result)

if __name__ == '__main__':
    main()
