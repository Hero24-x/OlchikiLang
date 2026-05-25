# -*- coding: utf-8 -*-

from programming.lexer import tokenize
from programming.parser import parse_lines


# =========================
# COMPILER ERROR
# =========================

class CompilerError(Exception):

    def __init__(self, stage, message):

        self.stage = stage
        self.message = message

        super().__init__(f"[{stage}] {message}")


# =========================
# COMPILER
# =========================

class Compiler:

    def __init__(self):

        # SOURCE
        self.source_code = ""

        # STAGES
        self.tokens = []
        self.ast = []

        # DEBUG
        self.debug = False

    # =========================
    # LOAD SOURCE
    # =========================

    def load(self, source_code):

        if not isinstance(source_code, str):

            raise CompilerError(
                "LOAD",
                "source code must be string"
            )

        self.source_code = source_code

    # =========================
    # LEXER STAGE
    # =========================

    def lex(self):

        try:

            self.tokens = tokenize(self.source_code)

            if self.debug:

                print("\\n===== TOKENS =====")

                for token in self.tokens:
                    print(token)

            return self.tokens

        except Exception as e:

            raise CompilerError(
                "LEXER",
                str(e)
            )

    # =========================
    # PARSER STAGE
    # =========================

    def parse(self):

        try:

            self.ast = parse_lines(self.tokens)

            if self.debug:

                print("\\n===== AST =====")

                for node in self.ast:
                    print(node)

            return self.ast

        except Exception as e:

            raise CompilerError(
                "PARSER",
                str(e)
            )

    # =========================
    # SEMANTIC ANALYSIS
    # =========================

    def semantic_analysis(self):

        """
        Future:
        - undefined variables
        - duplicate functions
        - type checking
        """

        return True

    # =========================
    # OPTIMIZER
    # =========================

    def optimize(self):

        """
        Future optimizer stage.
        """

        return self.ast

    # =========================
    # FULL COMPILATION
    # =========================

    def compile(self, source_code):

        self.load(source_code)

        self.lex()

        self.parse()

        self.semantic_analysis()

        self.optimize()

        return self.ast

    # =========================
    # DEBUG MODE
    # =========================

    def enable_debug(self):

        self.debug = True

    def disable_debug(self):

        self.debug = False

    # =========================
    # RESET
    # =========================

    def reset(self):

        self.tokens = []

        self.ast = []
