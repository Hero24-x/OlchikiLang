from programming.ast_nodes import (
    Print,
    SetVar,
    FunctionDef,
    FunctionCall,
    Return
)

from programming.vm import (
    eval_node,
    int_to_olchiki,
    variables,
    functions
)

# ================= RUN NODE =================

def run_node(node):

    if node is None:
        return None

    # ================= PRINT =================

    if isinstance(node, Print):

        result = eval_node(node.expr)

        print(int_to_olchiki(result))

        return result

    # ================= VARIABLE =================

    elif isinstance(node, SetVar):

        value = eval_node(node.expr)

        variables[node.name] = value

        return value

    # ================= RETURN =================

    elif isinstance(node, Return):

        return eval_node(node.value)

    # ================= FUNCTION DEFINE =================

    elif isinstance(node, FunctionDef):

        functions[node.name] = node

        return None

    # ================= FUNCTION CALL =================

    elif isinstance(node, FunctionCall):

        func = functions.get(node.name)

        if not func:
            print("❌ ᱵᱷᱩᱞ: function not found")
            return None

        old_vars = variables.copy()

        # ARGUMENT BINDING
        for param, arg in zip(func.params, node.args):

            variables[param] = eval_node(arg)

        result = None

        # RUN FUNCTION BODY
        for stmt in func.body:

            result = run_node(stmt)

            if isinstance(stmt, Return):
                break

        variables.clear()
        variables.update(old_vars)

        return result

    return None
