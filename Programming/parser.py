# -*- coding: utf-8 -*-

from programming.ast_nodes import (

    Number,
    String,
    Boolean,

    Variable,

    BinaryOp,
    UnaryOp,

    Print,
    SetVar,

    If,
    While,

    FunctionDef,
    FunctionCall,

    Return
)


# =========================================
# PARSER ERROR
# =========================================

class ParserError(Exception):

    pass


# =========================================
# PARSER
# =========================================

class Parser:

    def __init__(self, tokens):

        self.tokens = tokens

        self.pos = 0

    # =====================================
    # CURRENT
    # =====================================

    def current(self):

        if self.pos < len(self.tokens):
            return self.tokens[self.pos]

        return None

    # =====================================
    # ADVANCE
    # =====================================

    def advance(self):

        self.pos += 1

    # =====================================
    # EXPECT
    # =====================================

    def expect(self, token_type):

        token = self.current()

        if token is None:

            raise ParserError(
                f"Expected {token_type}, got EOF"
            )

        if token.type != token_type:

            raise ParserError(
                f"Expected {token_type}, "
                f"got {token.type}"
            )

        self.advance()

        return token

    # =====================================
    # MAIN PARSE
    # =====================================

    def parse(self):

        statements = []

        while self.current() is not None:

            stmt = self.parse_statement()

            if stmt:
                statements.append(stmt)

        return statements

    # =====================================
    # STATEMENT
    # =====================================

    def parse_statement(self):

        token = self.current()

        if token is None:
            return None

        # PRINT
        if token.type == "PRINT":
            return self.parse_print()

        # VARIABLE
        elif token.type == "SET":
            return self.parse_variable()

        # IF
        elif token.type == "IF":
            return self.parse_if()

        # WHILE
        elif token.type == "WHILE":
            return self.parse_while()

        # FUNCTION
        elif token.type == "FUNCTION":
            return self.parse_function()

        # RETURN
        elif token.type == "RETURN":
            return self.parse_return()

        # FUNCTION CALL
        elif token.type == "IDENTIFIER":

            expr = self.parse_expression()

            return expr

        raise ParserError(
            f"Unknown statement {token.type}"
        )

    # =====================================
    # BLOCK
    # =====================================

    def parse_block(self):

        statements = []

        self.expect("LBRACE")

        while (
            self.current()
            and self.current().type != "RBRACE"
        ):

            stmt = self.parse_statement()

            if stmt:
                statements.append(stmt)

        self.expect("RBRACE")

        return statements

    # =====================================
    # PRINT
    # =====================================

    def parse_print(self):

        self.expect("PRINT")

        expr = self.parse_expression()

        return Print(expr)

    # =====================================
    # VARIABLE
    # =====================================

    def parse_variable(self):

        self.expect("SET")

        name = self.expect(
            "IDENTIFIER"
        ).value

        self.expect("ASSIGN")

        expr = self.parse_expression()

        return SetVar(name, expr)

    # =====================================
    # IF
    # =====================================

    def parse_if(self):

        self.expect("IF")

        condition = self.parse_expression()

        body = self.parse_block()

        else_body = []

        if (
            self.current()
            and self.current().type == "ELSE"
        ):

            self.advance()

            else_body = self.parse_block()

        return If(
            condition,
            body,
            else_body
        )

    # =====================================
    # WHILE
    # =====================================

    def parse_while(self):

        self.expect("WHILE")

        condition = self.parse_expression()

        body = self.parse_block()

        return While(
            condition,
            body
        )

    # =====================================
    # FUNCTION
    # =====================================

    def parse_function(self):

        self.expect("FUNCTION")

        name = self.expect(
            "IDENTIFIER"
        ).value

        self.expect("LPAREN")

        params = []

        while (
            self.current()
            and self.current().type != "RPAREN"
        ):

            param = self.expect(
                "IDENTIFIER"
            ).value

            params.append(param)

            if (
                self.current()
                and self.current().type == "COMMA"
            ):

                self.advance()

        self.expect("RPAREN")

        body = self.parse_block()

        return FunctionDef(
            name,
            params,
            body
        )

    # =====================================
    # RETURN
    # =====================================

    def parse_return(self):

        self.expect("RETURN")

        expr = self.parse_expression()

        return Return(expr)

    # =====================================
    # PRIMARY
    # =====================================

    def parse_primary(self):

        token = self.current()

        if token is None:

            raise ParserError(
                "Unexpected EOF"
            )

        # NUMBER
        if token.type == "NUMBER":

            self.advance()

            return Number(token.value)

        # STRING
        elif token.type == "STRING":

            self.advance()

            return String(token.value)

        # BOOLEAN
        elif token.type == "TRUE":

            self.advance()

            return Boolean(True)

        elif token.type == "FALSE":

            self.advance()

            return Boolean(False)

        # UNARY
        elif token.type == "MINUS":

            self.advance()

            expr = self.parse_primary()

            return UnaryOp("-", expr)

        # IDENTIFIER / FUNCTION CALL
        elif token.type == "IDENTIFIER":

            self.advance()

            name = token.value

            # FUNCTION CALL
            if (
                self.current()
                and self.current().type == "LPAREN"
            ):

                self.advance()

                args = []

                while (
                    self.current()
                    and self.current().type != "RPAREN"
                ):

                    args.append(
                        self.parse_expression()
                    )

                    if (
                        self.current()
                        and self.current().type == "COMMA"
                    ):

                        self.advance()

                self.expect("RPAREN")

                return FunctionCall(
                    name,
                    args
                )

            return Variable(name)

        # PARENTHESIS
        elif token.type == "LPAREN":

            self.advance()

            expr = self.parse_expression()

            self.expect("RPAREN")

            return expr

        raise ParserError(
            f"Unexpected token {token.type}"
        )

    # =====================================
    # FACTOR
    # =====================================

    def parse_factor(self):

        left = self.parse_primary()

        while True:

            token = self.current()

            if (
                token
                and token.type in (
                    "MUL",
                    "DIV"
                )
            ):

                self.advance()

                right = self.parse_primary()

                left = BinaryOp(
                    left,
                    token.value,
                    right
                )

            else:
                break

        return left

    # =====================================
    # TERM
    # =====================================

    def parse_term(self):

        left = self.parse_factor()

        while True:

            token = self.current()

            if (
                token
                and token.type in (
                    "PLUS",
                    "MINUS"
                )
            ):

                self.advance()

                right = self.parse_factor()

                left = BinaryOp(
                    left,
                    token.value,
                    right
                )

            else:
                break

        return left

    # =====================================
    # COMPARISON
    # =====================================

    def parse_comparison(self):

        left = self.parse_term()

        while True:

            token = self.current()

            if (
                token
                and token.type in (

                    "EQ",
                    "NE",

                    "GT",
                    "LT",

                    "GTE",
                    "LTE"
                )
            ):

                self.advance()

                right = self.parse_term()

                left = BinaryOp(
                    left,
                    token.value,
                    right
                )

            else:
                break

        return left

    # =====================================
    # EXPRESSION
    # =====================================

    def parse_expression(self):

        return self.parse_comparison()
