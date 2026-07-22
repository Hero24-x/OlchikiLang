import re
import os
from decimal import Decimal, ROUND_HALF_UP, getcontext


getcontext().prec = 28

RED = "\033[91m"
RESET = "\033[0m"

variables = {}


booleans = {
    "ᱥᱟᱹᱨᱤ": True,
    "ᱵᱟᱝ": False
}


def ol_input(prompt):
    return input(prompt + " ")


def ol_len(text):
    return len(str(text))


def to_english(text):
    text = text.replace("⁻", "-")

    mapping = str.maketrans(
        "᱐᱑᱒᱓᱔᱕᱖᱗᱘᱙",
        "0123456789"
    )

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

        if isinstance(val, str):
            replacement = f'"{val}"'
        else:
            replacement = str(val)

        expr = re.sub(
            rf'\b{re.escape(v)}\b',
            replacement,
            expr
        )

    return expr



def safe_eval(expr):

    try:

        expr = replace_variables(expr)

        return eval(
            to_english(expr),
            {
                "__builtins__": None,
                "ᱡᱟᱹᱱᱟᱢ": ol_input,
                "ᱫᱤᱜ": ol_len,
                "ᱥᱟᱹᱨᱤ": True,
                "ᱵᱟᱝ": False
            },
            {}
        )


    except ZeroDivisionError:
        raise Exception("Division by zero")


    except SyntaxError:
        raise Exception("Invalid syntax")


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


        # CLEAR

        if line == "ᱥᱟᱯᱷᱟ":

            os.system(
                "cls" if os.name == "nt" else "clear"
            )

            return



        # VERSION

        if line == "ᱵᱷᱟᱨᱥᱚᱱ":

            print("ᱚᱞᱪᱤᱠᱤLang 1.0.0")
            print("HansdaTechs")

            return



        # HELP

        if line == "ᱜᱚᱡ":

            print("ᱚᱞᱪᱤᱠᱤLang Commands")
            print("ᱥᱮᱴ      -> Variable")
            print("ᱪᱷᱟᱯᱟ    -> Print")
            print("ᱡᱟᱹᱱᱟᱢ   -> Input")
            print("ᱫᱤᱜ     -> Length")
            print("ᱵᱷᱟᱨᱥᱚᱱ -> Version")
            print("ᱥᱟᱯᱷᱟ    -> Clear")
            print("ᱥᱮᱴ      ->  Set")

            return



        # VARIABLE SET

        if line.startswith("ᱥᱮᱴ"):


            if "=" not in line:
                raise Exception("Missing '='")


            parts = line.replace(
                "ᱥᱮᱴ",
                "",
                1
            ).split(
                "=",
                1
            )


            var_name = parts[0].strip()
            expr = parts[1].strip()


            if not re.fullmatch(
                r"[\u1C50-\u1CFF]+",
                var_name
            ):
                raise Exception(
                    "Only Ol Chiki variable names allowed"
                )


            # STRING

            if expr.startswith('"') and expr.endswith('"'):

                text = expr[1:-1]

                if not re.fullmatch(
                    r"[\u1C50-\u1CFF\s]+",
                    text
                ):
                    raise Exception(
                        "Only Ol Chiki text allowed"
                    )

                variables[var_name] = text

                return


            # NUMBER / EXPRESSION

            result = safe_eval(expr)

            variables[var_name] = result

            return





        # MEMORY CLEAR

        if line == "ᱢᱮᱢ":

            variables.clear()

            print("Memory Cleared")

            return





        # PRINT

        if line.startswith("ᱪᱷᱟᱯᱟ"):
            


            expr = line.replace(
                "ᱪᱷᱟᱯᱟ",
                "",
                1
            ).strip()



            # direct string

            if expr.startswith('"') and expr.endswith('"'):


                text = expr[1:-1]

                print(text)

                return





            # variable

            if expr in variables:

                value = variables[expr]

                if value == "True":
                    print("ᱥᱟᱹᱨᱤ")
                    return

                if value == "False":
                    print("ᱮᱲᱮ")
                    return

                print(
                    to_olchiki(value)
                )

                return





            # expression

            result = safe_eval(expr)

            if isinstance(result, str):
                print(result)
                return

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





          # IF V2
        if line.startswith("ᱡᱩᱫᱤ"):

            condition = line.replace(
                "ᱡᱩᱫᱤ",
                "",
                1
            ).strip()

            return bool(
                safe_eval(condition)
            )


        # LOOP PLACEHOLDER

        if line.startswith("ᱞᱮᱛ"):

            count =line.replace(
                "ᱞᱮᱛ",
                "",
                1
            ).strip()

            count = int(
                to_english(count)

            )

            for i in range(count):
                print(
                    to_olchiki(i + 1)
                )

            return


        raise Exception(
            f"Invalid Command: {line}"
        )



    except Exception as e:

        print(
            f"{RED}❌ {e}{RESET}"
        )
