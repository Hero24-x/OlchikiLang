import sys
import os

from updater import check_updates
from spl.parser import parse_lines, to_english, RED, RESET


YELLOW = "\033[93m"
GREEN = "\033[92m"
RESET = "\033[0m"


BLOCK_COMMANDS = [
    "ᱡᱩᱫᱤ"
]

BLOCK_END = "ᱢᱩᱪ"
ELSE_COMMAND = "ᱵᱟᱝ"


def is_block_command(line):
    return any(line.startswith(cmd) for cmd in BLOCK_COMMANDS)

check_updates()

def run_file(filename):
    if not os.path.exists(filename):
        print(f"{RED}File not found:{filename}{RESET}")
        return

    with open(filename, "r", encoding="utf-8") as file:
        lines = file.readlines()

    for line in lines:
        line = line.strip()

        if line:
            parse_lines(line)

        if len(sys.argv) > 1:
            run_file(sys.argv[1])
            exit()

print("------------------------------------------")
print(" ᱚᱞᱪᱤᱠᱤLang 1.0.0 [HansdaTechs] ")
print(" Santali Programming Language ")
print(" Commands: ᱵᱷᱟᱨᱥᱚᱱ, ᱥᱟᱯᱷᱟ, ᱜᱚᱡ, ᱰᱟᱦᱮ ")
print("------------------------------------------")


while True:
    try:

        user_input = input(f"{YELLOW}ᱦᱟᱸᱥᱫᱟ{RESET} {GREEN}>>>{RESET}").strip()

        if not user_input:
            continue

        if user_input.startswith("#"):
            continue


        # EXIT
        if user_input == "ᱰᱟᱦᱮ":
            print("ᱰᱟᱦᱮ...")
            break


        # IF BLOCK
        if is_block_command(user_input):

            block_true = []
            block_false = []

            condition = user_input.replace(
                "ᱡᱩᱫᱤ",
                "",
                1
            ).strip()

            result = parse_lines(
                "ᱡᱩᱫᱤ " + condition
            )

            current = block_true

            while True:

                line = input("    ").strip()

                if line == BLOCK_END:
                    break

                if line == ELSE_COMMAND:
                    current = block_false
                    continue

                if line:
                    current.append(line)


            if result:

                for cmd in block_true:
                    parse_lines(cmd)

            else:

                for cmd in block_false:
                    parse_lines(cmd)

            continue


        # LOOP
        if user_input.startswith("ᱞᱮᱛ"):

            try:
                parts = user_input.split()

                count = int(to_english(parts[1]))

                command = input("    ").strip()

                for _ in range(count):
                    parse_lines(command)

            except Exception:
                print(
                    f"{RED}❌ Syntax Error: Use ᱞᱮᱛ <number>{RESET}"
                )

            continue



        if user_input.startswith(
            (
            "ᱥᱮᱴ",
            "ᱪᱷᱟᱯᱟ",
            "ᱵᱷᱟᱨᱥᱚᱱ",
            "ᱥᱟᱯᱷᱟ",
            "ᱜᱚᱡ",
            "ᱢᱮᱢ"
            )
        ):
            parse_lines(user_input)

        else:
            parse_lines("ᱪᱷᱟᱯᱟ " + user_input)



    except KeyboardInterrupt:
        print(
            f"\n{RED}❌ Process interrupted! Type ᱰᱟᱦᱮ to quit.{RESET}"
        )


    except Exception as e:
        print(
            f"{RED}❌ Error: {e}{RESET}"
        )
