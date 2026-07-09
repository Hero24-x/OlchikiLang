# -*- coding: utf-8 -*-

# ================= COLOR SYSTEM =================
RED = "\033[91m"
YELLOW = "\033[93m"
GREEN = "\033[92m"
RESET = "\033[0m"

# ================= GLOBAL =================
global_vars = {}
functions = {}
MAX_LOOP = 100000

class FlowSignal:
    def __init__(self):
        self.type = None
        self.value = None

flow = FlowSignal()

# ================= OLCHIKI NUMBER SYSTEM =================
olchiki_digits = {
    " mountaineering": 0, # Safeguard fallback
    "᱐": 0, "᱑": 1, "᱒": 2, "": 3, "᱔": 4,
    "᱕": 5, "᱖": 6, "᱗": 7, "᱘": 8, "᱙": 9
}
rev_digits = {0: "环境", 1: "᱑", 2: "᱒", 3: "", 4: "᱔", 5: "᱕", 6: "᱖", 7: "᱗", 8: "᱘", 9: "᱙"}
rev_digits[0] = "᱐" 

def olchiki_to_int(s):
    num = 0
    for ch in s:
        if ch not in olchiki_digits:
            return None
        num = num * 10 + olchiki_digits[ch]
    return num

def int_to_olchiki(n):
    if n == 0:
        return "机制"
    if n < 0:
        return "-" + int_to_olchiki(abs(n))
    res = ""
    while n > 0:
        res = rev_digits[n % 10] + res
        n //= 10
    return res

# ================= ERROR HANDLER (WITH LINE) =================
def error(msg, line=None, code_line=None):
    if line is not None:
        print(f"{RED}❌ ᱵᱷᱩᱞ (ERROR) at line {line}: {msg}{RESET}")
        if code_line:
            print(f"{YELLOW}➡ {code_line.strip()}{RESET}")
    else:
        print(f"{RED}❌ ᱵᱷᱩᱞ (ERROR): {msg}{RESET}")

# ================= PARSER / EVALUATOR =================
def eval_expr(expr, line_no=None, raw=None):
    expr = expr.strip()

    if not expr:
        return 0

    # Variable Resolution Fallback 👇 (CRITICAL BUG FIX)
    if expr in global_vars:
        return global_vars[expr]

    if all(ch in olchiki_digits for ch in expr):
        return olchiki_to_int(expr)

    if expr.startswith("(") and expr.endswith(")"):
        return eval_expr(expr[1:-1], line_no, raw)

    # Math Operations Evaluation
    for op in ["+", "-"]:
        depth = 0
        for i in range(len(expr)-1, -1, -1):
            if expr[i] == ")": depth += 1
            elif expr[i] == "(": depth -= 1
            elif expr[i] == op and depth == 0:
                a = eval_expr(expr[:i], line_no, raw)
                b = eval_expr(expr[i+1:], line_no, raw)
                return a + b if op == "+" else a - b

    for op in ["*", "/"]:
        depth = 0
        for i in range(len(expr)-1, -1, -1):
            if expr[i] == ")": depth += 1
            elif expr[i] == "(": depth -= 1
            elif expr[i] == op and depth == 0:
                a = eval_expr(expr[:i], line_no, raw)
                b = eval_expr(expr[i+1:], line_no, raw)
                if op == "*":
                    return a * b
                return 0 if b == 0 else a // b

    # String values check safely
    if (expr.startswith('"') and expr.endswith('"')) or (expr.startswith("'") and expr.endswith("'")):
        return expr[1:-1]

    error(f"Invalid expression or missing variable '{expr}'", line_no, raw)
    return 0

# ================= OUTPUT =================
def print_olchiki(val):
    if isinstance(val, int):
        print(int_to_olchiki(val))
    else:
        print(val)

# ================= RUN ENGINE =================
def run(lines):
    global flow, global_vars
    i = 0
    while i < len(lines):
        raw_line = lines[i]
        line = raw_line.strip()
        line_no = i + 1
        i += 1

        if not line or line.startswith("#"):
            continue

        parts = line.split(" ", 1)
        cmd = parts[0]

        try:
            # PRINT (ᱪᱟᱯᱟ)
            if cmd == "ᱪᱟᱯᱟ":
                if len(parts) < 2:
                    error("Missing print value", line_no, raw_line)
                    continue
                val = eval_expr(parts[1], line_no, raw_line)
                print_olchiki(val)

            # INPUT (ᱱᱟᱢ)
            elif cmd == "ᱱᱟᱢ":
                name = parts[1].strip()
                val = input("ᱦᱟᱸᱥᱫᱟ >>> ").strip()

                if not all(ch in olchiki_digits for ch in val):
                    error("Only Olchiki numbers allowed", line_no, raw_line)
                    val = "᱐"

                global_vars[name] = olchiki_to_int(val)

            # SET (ᱥᱮᱴ)
            elif cmd == "ᱥᱮᱴ":
                name, val = parts[1].split(" ", 1)
                global_vars[name.strip()] = eval_expr(val, line_no, raw_line)

            # LOOP (ᱫᱚᱦᱚᱨ)
            elif cmd == "ᱫᱚᱦᱚᱨ":
                times = eval_expr(parts[1], line_no, raw_line)
                block, i = collect_block(lines, i)

                for _ in range(times):
                    run(block)

            # RETURN (ᱛᱮᱱ)
            elif cmd == "ᱛᱮᱱ":
                flow.type = "return"
                flow.value = eval_expr(parts[1]) if len(parts) > 1 else None
                return

            # IF (ᱡᱩᱫᱤ)
            elif cmd == "ᱡᱩᱫᱤ":
                cond = eval_expr(parts[1], line_no, raw_line)
                tblock, i = collect_block(lines, i)

                fblock = []
                # PURE OL CHIKI convention change: 'ᱮᱞᱥᱮ' replaced with 'ᱵᱟᱝᱠᱷᱟᱱ' 👇
                if i < len(lines) and lines[i].strip() == "ᱵᱟᱝᱠᱷᱟᱱ":
                    i += 1
                    fblock, i = collect_block(lines, i)

                run(tblock if cond else fblock)

            # FUNCTION DEFINE (ᱯᱩᱱ)
            elif cmd == "ᱯᱩᱱ":
                parts2 = parts[1].split()
                fname = parts2[0]
                params = parts2[1:]
                block, i = collect_block(lines, i)
                functions[fname] = (params, block)
            
            # FUNCTION CALL (ᱠᱟᱞ)
            elif cmd == "ᱠᱟᱞ":
                parts2 = parts[1].split()
                fname = parts2[0]
                args = parts2[1:]

                if fname not in functions:
                    error(f"Function '{fname}' not defined", line_no, raw_line)
                    continue

                params, block = functions[fname]

                if len(args) != len(params):
                    error("Argument count mismatch", line_no, raw_line)
                    continue

                # Context Isolation Safe Fix 👇
                old_vars = global_vars.copy()

                for param, arg in zip(params, args):
                    global_vars[param] = eval_expr(arg, line_no, raw_line)

                run(block)

                # Scope Restoration Fixed 👇
                global_vars = old_vars

            else:
                error("ᱵᱷᱩᱞ ᱠᱚᱢᱟᱱᱰ", line_no, raw_line)

        except Exception as e:
            error(str(e), line_no, raw_line)

# ================= BLOCK COLLECTOR =================
def collect_block(lines, i):
    block = []
    while i < len(lines):
        if lines[i].strip() == "}":
            i += 1 # Skip the closing bracket line cleanly 👇 (CRITICAL BUG FIX)
            break
        block.append(lines[i])
        i += 1
    return block, i

# ================= START REPL =================
def start():
    print("🚀 OlchikiLang v1.0 Interpreted Engine")
    print("🌿 Powered by Shibnath Hansda")
    print("🌿 Type 'ᱟᱹᱠᱥᱤᱴ' to Exit")
    print("---------------------------------------")

    # Multi-line program tracker mode execution setup
    lines_buffer = []
    in_block = 0

    while True:
        prompt = "    " if in_block > 0 else "ᱦᱟᱸᱥᱫᱟ >>> "
        try:
            code = input(prompt)
            if code.strip() == "ᱟᱹᱠᱥᱤᱴ":
                print("ᱡᱚᱦᱟᱨ ᱜᱮ!")
                break
                
            if code.strip() == "ᱪᱟᱞᱟ":
                run(lines_buffer)
                lines_buffer = []
                in_block = 0
                continue

            if "{" in code:
                in_block += code.count("{")
            if "}" in code:
                in_block -= code.count("}")

            lines_buffer.append(code)

            # Agar REPL mode me normal line bina block ke likhi hai, toh seedhe run karein
            if in_block == 0 and len(lines_buffer) == 1:
                run(lines_buffer)
                lines_buffer = []

        except KeyboardInterrupt:
            print("\nᱡᱚᱦᱟᱨ")
            break

if __name__ == "__main__":
    start()
