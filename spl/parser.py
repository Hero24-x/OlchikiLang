import re
import os
from decimal import Decimal, ROUND_HALF_UP, getcontext

getcontext().prec = 28

RED = "\033[91m"
RESET = "\033[0m"

variables = {}

def to_english(text):
    text = text.replace("⁻", "-")
    mapping = str.maketrans("᱐᱑᱒᱓᱔᱕᱖᱗᱘᱙", "0123456789")
    return text.translate(mapping)


def to_olchiki(text):
    text = str(text)

    mapping = {
        "0":"᱐",
        "1":"᱑",
        "2":"᱒",
        "3":"᱓",
        "4":"᱔",
        "5":"᱕",
        "6":"᱖",
        "7":"᱗",
        "8":"᱘",
        "9":"᱙"
    }

    for e, o in mapping.items():
        text = text.replace(e, o)

    return text


def replace_variables(expr):
    for v, val in sorted(
        variables.items(),
        key=lambda x: len(x[0]),
        reverse=True
    ):
        expr = re.sub(
            rf'\b{re.escape(v)}\b',
            str(val),
            expr
        )

    return expr


def safe_eval(expr):
    try:
        expr = replace_variables(expr)
        return eval(
            to_english(expr),
            {"__builtins__": None},
            {}
        )

    except ZeroDivisionError:
        raise Exception("Division by zero")

    except SyntaxError:
        raise Exception("Invalid syntax")

    except NameError:
        raise Exception("Unknown variable")

    except Exception:
        raise Exception("Invalid expression")


def parse_lines(line):
    global variables

    line = line.strip()

    if not line:
        return

    if "#" in line:
        line = line.split("#")[0].strip()

    if not line:
        return

    try:

        if line == "ᱥᱟᱯᱷᱟ":
            os.system("cls" if os.name == "nt" else "clear")
            return


        if line == "ᱵᱷᱟᱨᱥᱚᱱ":
            print("OlChikiLang 1.0")
            print("Disom Labs")
            return


        if line == "ᱜᱚᱡ":
            variables.clear()
            print("Memory Cleared")
            return


        if line.startswith("ᱥᱮᱴ"):

            if "=" not in line:
                raise Exception("Missing '='")

            parts = line.replace("ᱥᱮᱴ", "", 1).split("=", 1)

            var_name = parts[0].strip()
            expr = parts[1].strip()

            result = safe_eval(expr)

            variables[var_name] = str(result)

            return


        elif line.startswith("ᱪᱟᱯᱟ"):

            expr = line.replace("ᱪᱟᱯᱟ", "", 1).strip()


            if (
                expr.startswith('"')
                and
                expr.endswith('"')
            ):
                print(expr[1:-1])
                return


            if expr in variables:
                print(
                    to_olchiki(
                        variables[expr]
                    )
                )
                return


            result = safe_eval(expr)

            d = Decimal(
                str(result)
            ).quantize(
                Decimal("1.0000000000"),
                rounding=ROUND_HALF_UP
            ).normalize()

            print(
                to_olchiki(
                    "{:f}".format(d)
                )
            )

            return


        elif line.startswith("ᱡᱩᱫᱤ"):
            print("❌ IF support coming soon")
            return


        elif line.startswith("ᱞᱮᱛ"):
            print("❌ LOOP support coming soon")
            return


        else:
            raise Exception(
                f"Invalid Command: {line}"
            )


    except Exception as e:
        print(
            f"{RED}❌ {e}{RESET}"
        )
