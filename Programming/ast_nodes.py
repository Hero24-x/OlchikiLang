# -*- coding: utf-8 -*-

# =========================================
# BASE NODE
# =========================================

class Node:

    def __init__(self):

        # future:
        # line number
        # column number
        self.line = None
        self.col = None

    def set_position(self, line, col):

        self.line = line
        self.col = col

        return self

    def position(self):

        if self.line is None:
            return ""

        return f"(line={self.line}, col={self.col})"


# =========================================
# EXPRESSIONS
# =========================================

class Number(Node):

    def __init__(self, value):

        super().__init__()

        self.value = value

    def __repr__(self):

        return (
            f"Number("
            f"value={self.value}"
            f")"
        )


class String(Node):

    def __init__(self, value):

        super().__init__()

        self.value = value

    def __repr__(self):

        return (
            f"String("
            f"value='{self.value}'"
            f")"
        )


class Boolean(Node):

    def __init__(self, value):

        super().__init__()

        self.value = value

    def __repr__(self):

        return (
            f"Boolean("
            f"value={self.value}"
            f")"
        )


class Variable(Node):

    def __init__(self, name):

        super().__init__()

        self.name = name

    def __repr__(self):

        return (
            f"Variable("
            f"name='{self.name}'"
            f")"
        )


class BinaryOp(Node):

    def __init__(self, left, op, right):

        super().__init__()

        self.left = left
        self.op = op
        self.right = right

    def __repr__(self):

        return (
            f"BinaryOp("
            f"left={self.left}, "
            f"op='{self.op}', "
            f"right={self.right}"
            f")"
        )


class UnaryOp(Node):

    def __init__(self, op, expr):

        super().__init__()

        self.op = op
        self.expr = expr

    def __repr__(self):

        return (
            f"UnaryOp("
            f"op='{self.op}', "
            f"expr={self.expr}"
            f")"
        )


# =========================================
# STATEMENTS
# =========================================

class Print(Node):

    def __init__(self, expr):

        super().__init__()

        self.expr = expr

    def __repr__(self):

        return (
            f"Print("
            f"expr={self.expr}"
            f")"
        )


class SetVar(Node):

    def __init__(self, name, expr):

        super().__init__()

        self.name = name
        self.expr = expr

    def __repr__(self):

        return (
            f"SetVar("
            f"name='{self.name}', "
            f"expr={self.expr}"
            f")"
        )


class Block(Node):

    def __init__(self, statements):

        super().__init__()

        self.statements = statements

    def __repr__(self):

        return (
            f"Block("
            f"statements={len(self.statements)}"
            f")"
        )


class If(Node):

    def __init__(
        self,
        condition,
        body,
        else_body=None
    ):

        super().__init__()

        self.condition = condition
        self.body = body

        if else_body is None:
            else_body = []

        self.else_body = else_body

    def __repr__(self):

        return (
            f"If("
            f"condition={self.condition}, "
            f"body={len(self.body)}, "
            f"else_body={len(self.else_body)}"
            f")"
        )


class While(Node):

    def __init__(self, condition, body):

        super().__init__()

        self.condition = condition
        self.body = body

    def __repr__(self):

        return (
            f"While("
            f"condition={self.condition}, "
            f"body={len(self.body)}"
            f")"
        )


# =========================================
# FUNCTIONS
# =========================================

class FunctionDef(Node):

    def __init__(
        self,
        name,
        params,
        body
    ):

        super().__init__()

        self.name = name
        self.params = params
        self.body = body

    def __repr__(self):

        return (
            f"FunctionDef("
            f"name='{self.name}', "
            f"params={self.params}, "
            f"body={len(self.body)}"
            f")"
        )


class FunctionCall(Node):

    def __init__(self, name, args):

        super().__init__()

        self.name = name
        self.args = args

    def __repr__(self):

        return (
            f"FunctionCall("
            f"name='{self.name}', "
            f"args={self.args}"
            f")"
        )


class Return(Node):

    def __init__(self, value):

        super().__init__()

        self.value = value

    def __repr__(self):

        return (
            f"Return("
            f"value={self.value}"
            f")"
        )


# =========================================
# MODULE SYSTEM
# =========================================

class Import(Node):

    def __init__(self, module):

        super().__init__()

        self.module = module

    def __repr__(self):

        return (
            f"Import("
            f"module='{self.module}'"
            f")"
        )


# =========================================
# EXCEPTION SYSTEM
# =========================================

class TryCatch(Node):

    def __init__(
        self,
        try_body,
        error_name,
        catch_body
    ):

        super().__init__()

        self.try_body = try_body
        self.error_name = error_name
        self.catch_body = catch_body

    def __repr__(self):

        return (
            f"TryCatch("
            f"error='{self.error_name}'"
            f")"
        )


# =========================================
# OBJECT ORIENTED PROGRAMMING
# =========================================

class ClassDef(Node):

    def __init__(self, name, body):

        super().__init__()

        self.name = name
        self.body = body

    def __repr__(self):

        return (
            f"ClassDef("
            f"name='{self.name}'"
            f")"
        )


class ObjectCreate(Node):

    def __init__(self, class_name):

        super().__init__()

        self.class_name = class_name

    def __repr__(self):

        return (
            f"ObjectCreate("
            f"class='{self.class_name}'"
            f")"
        )
