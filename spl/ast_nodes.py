class Node:
    pass


class Print(Node):
    def __init__(self, expr):
        self.expr = expr


# ✅ New: Input Node for 'ᱱᱟᱢ' keyword support in AST mode
class Input(Node):
    def __init__(self, name):
        self.name = name


class SetVar(Node):
    def __init__(self, name, expr):
        self.name = name
        self.expr = expr


class If(Node):
    def __init__(self, cond, body, else_body=None):
        self.cond = cond
        self.body = body
        self.else_body = else_body


class Loop(Node):
    def __init__(self, times, body):
        self.times = times
        self.body = body


# ✅ ONLY ONE FUNCTION SYSTEM (KEEP THIS)
class FunctionDef(Node):
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body


class FunctionCall(Node):
    def __init__(self, name, args):
        self.name = name
        self.args = args


class Return(Node):
    def __init__(self, value):
        self.value = value
