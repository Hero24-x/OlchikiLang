import os
import re
import subprocess
import sys
import math
from .ast_nodes import (
    Print, SetVar, FunctionDef, FunctionCall, Return, If, Loop, Input 
)

RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RESET = "\033[0m"

variables = {}
functions = {}

olchiki_to_ascii = {
    "᱐": "0", "᱑": "1", "᱒": "2", "᱓": "3", "᱔": "4",
    "᱕": "5", "᱖": "6", "᱗": "7", "᱘": "8", "᱙": "9",

    # Fallback (English numbers)
    "0": "0", "1": "1", "2": "2", "3": "3", "4": "4",
    "5": "5", "6": "6", "7": "7", "8": "8", "9": "9",

    # 🔥 Silent Safety Guard: Back-end me '3' convert karega, crash se bachayega
    "": "3" 
}

ascii_to_olchiki = {
    "0": "᱐",
    "1": "᱑",
    "2": "᱒",
    "3": "᱓",  # 🔥 Output me HAMESHA sirf yehi perfect standard character dikhega!
    "4": "᱔",
    "5": "᱕",
    "6": "᱖",
    "7": "᱗",
    "8": "᱘",
    "9": "᱙"
}

def to_olchiki_str(val):
    val_str = str(val)
    return "".join(ascii_to_olchiki.get(char, char) for char in val_str)

def eval_expr(expr):
    if isinstance(expr, list): 
        expr = " ".join(str(x) for x in expr)
    
    expr_str = str(expr).replace("ᱥᱟᱹᱨᱤ", "True").replace("ᱵᱟᱝ", "False")
    
    # 🔬 Full Power Science & Math Mapping Interceptor
    if "ᱨᱮᱦᱮᱫ" in expr_str: expr_str = expr_str.replace("ᱨᱮᱦᱮᱫ", "math.sqrt")
    if "ᱜᱟᱵᱟᱱ" in expr_str: expr_str = expr_str.replace("ᱜᱟᱵᱟᱱ", "math.pow")
    if "ᱥᱟᱭᱤᱱ" in expr_str: expr_str = expr_str.replace("ᱥᱟᱭᱤᱱ", "math.sin")
    if "ᱠᱳᱥ" in expr_str:   expr_str = expr_str.replace("ᱠᱳᱥ", "math.cos")
    if "ᱞᱚᱜ" in expr_str:   expr_str = expr_str.replace("ᱞᱚᱜ", "math.log10")
    if "ᱯᱟᱭ" in expr_str:   expr_str = expr_str.replace("ᱯᱟᱭ", "math.pi")
    if "ᱡᱮᱞ" in expr_str:   expr_str = expr_str.replace("ᱡᱮᱞ", "len")
        
    expr_str = expr_str.replace(" ", "")
    
    for k, v in olchiki_to_ascii.items(): 
        expr_str = expr_str.replace(k, v)
        
    try:
        safe_builtins = {
            "len": len, "int": int, "float": float, "str": str, "list": list,
            "math": math
        }
        return eval(expr_str, {"__builtins__": safe_builtins}, variables)
    except Exception as e:
        return variables.get(expr, expr)

# 🔥 Pure Ol Chiki Package Auto Installer Utility
def handle_package_install(pkg_name):
    try:
        print(YELLOW + "⏳ ᱯᱮᱠᱮᱡᱽ ᱰᱟᱩᱱᱞᱚᱰ ᱠᱟᱱᱟ..." + RESET)
        subprocess.check_call([sys.executable, "-m", "pip", "install", pkg_name], 
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(GREEN + "✔ ᱠᱟᱹᱢᱤ ᱯᱩᱨᱟᱹᱣ ᱮᱱᱟ" + RESET)
        return True
    except Exception:
        print(RED + "❌ ᱵᱷᱩᱞ: ᱯᱮᱠᱮᱡᱽ ᱵᱟᱝ ᱤᱱᱥᱴᱚᱞ ᱞᱮᱱᱟ" + RESET)
        return False

def run_node(node):
    global variables
    if node is None: return None
    try:
        line_str = str(node.expr if hasattr(node, 'expr') else node).strip()
        
        # ---------------- 📦 ᱵᱮᱵᱷᱟᱨ (Package Installer Engine) ----------------
        if line_str.startswith("ᱵᱮᱵᱷᱟᱨ"):
            tokens = line_str.split()
            if len(tokens) >= 2:
                pkg_name = tokens[1].strip()
                return handle_package_install(pkg_name)
            print(RED + "❌ ᱵᱷᱩᱞ: ᱯᱮᱠᱮᱡᱽ ᱧᱩᱛᱩᱢ ᱵᱟᱝ ᱧᱟᱢ ᱞᱮᱱᱟ" + RESET)
            return False

        # 1. ᱡᱩᱲ (Append) Check
        if (isinstance(node, FunctionCall) and node.name == "ᱡᱩᱲ") or (isinstance(node, str) and line_str.startswith("ᱡᱩᱲ")):
            line_str = line_str.replace(" ", "")
            content = line_str[line_str.find("(")+1 : line_str.rfind(")")]
            parts = content.split(",")
            if len(parts) >= 2:
                ln = parts[0].strip()
                val = eval_expr(parts[1].strip())
                if ln in variables and isinstance(variables[ln], list):
                    variables[ln].append(val)
                    return True
            print(RED + "❌ ᱵᱷᱩᱞ: ᱡᱩᱲ ᱵᱟᱝ ᱵᱮᱵᱷᱟᱨ ᱞᱮᱱᱟ" + RESET)
            return False

        # 2. ᱚᱪᱚ (Remove) Check
        elif (isinstance(node, FunctionCall) and node.name == "ᱚᱪᱚ") or (isinstance(node, str) and line_str.startswith("ᱚᱪᱚ")):
            line_str = line_str.replace(" ", "")
            content = line_str[line_str.find("(")+1 : line_str.rfind(")")]
            parts = content.split(",")
            if len(parts) >= 2:
                ln = parts[0].strip()
                idx = int(eval_expr(parts[1].strip()))
                if ln in variables and isinstance(variables[ln], list):
                    try:
                        variables[ln].pop(idx)
                        return True
                    except IndexError:
                        print(RED + "❌ ᱵᱷᱩᱞ: Index Out of Bounds" + RESET)
                        return False
            print(RED + "❌ ᱵᱷᱩᱞ: ᱚᱪᱚ ᱵᱟᱝ ᱵᱮᱵᱷᱟᱨ ᱞᱮᱱᱟ" + RESET)
            return False

        if not all ('0'<= c <= '"' or c.isspace() for c in val ):
            print ("❌ ᱵᱷᱩᱞ")
            return True
            
        elif isinstance(node, Input):
            val = input("ᱦᱟᱸᱥᱫᱟ >>> ").strip()
            variables[node.name] = val
            return True
            
        elif isinstance(node, SetVar):
            if not re.match(r'^[\u1c50-\u1c7f]+$', node.name):
                print(RED + f"❌ ᱵᱷᱩᱞ: ᱵᱟᱝ ᱥᱟᱵᱟᱫ ᱧᱩᱛᱩᱢ '{node.name}'" + RESET)
                return False
            variables[node.name] = eval_expr(node.expr)
            return True
            
        elif isinstance(node, FunctionCall):
            func = functions.get(node.name)
            if not func:
                print(RED + f"❌ ᱵᱷᱩᱞ: ᱯᱷᱟᱱᱠᱥᱚᱱ ᱵᱟᱝ ᱧᱟᱢ ᱞᱮᱱᱟ ({node.name})" + RESET)
                return False
            return True
            
        # 🔥 PERFECTLY ALIGNED REPL FALLBACK
        else:
            if hasattr(node, '__class__') and node.__class__.__name__ in ['Loop', 'If', 'FunctionDef']:
                return True
                
            if line_str.startswith("ᱡᱩᱲ"):
                content = line_str[min(line_str.find("(")+1, len(line_str)):line_str.rfind(")")]
                parts = content.split(",")
                if len(parts) >= 2:
                    ln = parts[0].strip()
                    val = eval_expr(parts[1].strip())
                    if ln in variables and isinstance(variables[ln], list):
                        variables[ln].append(val)
                        return True
            
            val = eval_expr(node)
            if val is not None and str(val) != line_str:
                print(to_olchiki_str(val))
            return True
            
    except Exception as e:
        print(RED + f"❌ [VM ᱵᱷᱩᱞ]: {e}" + RESET)
        return False
