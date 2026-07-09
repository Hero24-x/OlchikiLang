import sys

from spl.compiler import compile_code, Print, SetVar, Return, FunctionDef, FunctionCall, int_to_olchiki
from spl.vm import eval_expr

variables = {}
functions = {}


def run_node(node):

    global return_value
    return_value = None

    if node is None:
        return None

    # PRINT
    if isinstance(node, Print):
        result = eval_expr(node.expr)
        print(int_to_olchiki(result))

    # SET VARIABLE
    elif isinstance(node, SetVar):
        variables[node.name] = eval_expr(node.expr)

    # RETURN
    elif isinstance(node, Return):
        return eval_expr(node.value)

    # FUNCTION DEF
    elif isinstance(node, FunctionDef):
        functions[node.name] = node

    # FUNCTION CALL
    elif isinstance(node, FunctionCall):

        func = functions.get(node.name)

        if not func:
            print("❌ ᱵᱷᱩᱞ: function not found")
            return None

        local_vars = dict(zip(func.params, node.args))

        old_vars = variables.copy()
        variables.update(local_vars)

        result = None

        for line in func.body:
            result = run_node(line)

            # 🔥 STOP if return found
            if isinstance(line, Return):
                variables.clear()
                variables.update(old_vars)
                return result

        variables.clear()
        variables.update(old_vars)

        return result
