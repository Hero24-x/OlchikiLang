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
# RUNTIME ERROR
# =========================================

class RuntimeError(Exception):

    pass


# =========================================
# INTERPRETER
# =========================================

class Interpreter:

    def __init__(self):

        # GLOBAL SCOPE
        self.variables = {}

        # FUNCTION TABLE
        self.functions = {}

    # =====================================
    # EVALUATE EXPRESSION
    # =====================================

    def eval(self, node):

        if node is None:
            return None

        # ================= NUMBER

        if isinstance(node, Number):

            return node.value

        # ================= STRING

        elif isinstance(node, String):

            return node.value

        # ================= BOOLEAN

        elif isinstance(node, Boolean):

            return node.value

        # ================= VARIABLE

        elif isinstance(node, Variable):

            if node.name not in self.variables:

                raise RuntimeError(
                    f"Undefined variable '{node.name}'"
                )

            return self.variables[node.name]

        # ================= UNARY

        elif isinstance(node, UnaryOp):

            value = self.eval(node.expr)

            if node.op == "-":
                return -value

            raise RuntimeError(
                f"Unknown unary operator {node.op}"
            )

        # ================= BINARY

        elif isinstance(node, BinaryOp):

            left = self.eval(node.left)

            right = self.eval(node.right)

            # ---------- MATH

            if node.op == "+":
                return left + right

            elif node.op == "-":
                return left - right

            elif node.op == "*":
                return left * right

            elif node.op == "/":

                if right == 0:

                    raise RuntimeError(
                        "Division by zero"
                    )

                return left // right

            # ---------- COMPARISON

            elif node.op == "==":
                return left == right

            elif node.op == "!=":
                return left != right

            elif node.op == ">":
                return left > right

            elif node.op == "<":
                return left < right

            elif node.op == ">=":
                return left >= right

            elif node.op == "<=":
                return left <= right

            raise RuntimeError(
                f"Unknown operator {node.op}"
            )

        # ================= FUNCTION CALL

        elif isinstance(node, FunctionCall):

            return self.call_function(node)

        raise RuntimeError(
            f"Invalid expression node {node}"
        )

    # =====================================
    # EXECUTE STATEMENT
    # =====================================

    def execute(self, node):

        if node is None:
            return None

        # ================= PRINT

        if isinstance(node, Print):

            value = self.eval(node.expr)

            print(value)

            return None

        # ================= VARIABLE

        elif isinstance(node, SetVar):

            value = self.eval(node.expr)

            self.variables[node.name] = value

            return None

        # ================= IF

        elif isinstance(node, If):

            condition = self.eval(node.condition)

            if condition:

                for stmt in node.body:
                    self.execute(stmt)

            else:

                for stmt in node.else_body:
                    self.execute(stmt)

            return None

        # ================= WHILE

        elif isinstance(node, While):

            while self.eval(node.condition):

                for stmt in node.body:
                    self.execute(stmt)

            return None

        # ================= FUNCTION DEF

        elif isinstance(node, FunctionDef):

            self.functions[node.name] = node

            return None

        # ================= RETURN

        elif isinstance(node, Return):

            return self.eval(node.value)

        # ================= FUNCTION CALL

        elif isinstance(node, FunctionCall):

            return self.call_function(node)

        raise RuntimeError(
            f"Unknown statement node {node}"
        )

    # =====================================
    # FUNCTION CALL
    # =====================================

    def call_function(self, node):

        if node.name not in self.functions:

            raise RuntimeError(
                f"Function '{node.name}' not found"
            )

        func = self.functions[node.name]

        # SAVE SCOPE
        old_scope = self.variables.copy()

        # BIND PARAMETERS
        for param, arg in zip(
            func.params,
            node.args
        ):

            self.variables[param] = self.eval(arg)

        result = None

        # EXECUTE BODY
        for stmt in func.body:

            result = self.execute(stmt)

            if isinstance(stmt, Return):
                break

        # RESTORE SCOPE
        self.variables = old_scope

        return result

    # =====================================
    # RUN PROGRAM
    # =====================================

    def run(self, ast):

        for node in ast:

            self.execute(node)
