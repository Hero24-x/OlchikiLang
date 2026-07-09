from updater import check_updates
from spl.parser import parse_lines, to_english, RED, RESET


BLOCK_COMMANDS = [
    "ᱡᱩᱫᱤ"
]

BLOCK_END = "ᱢᱩᱪ"


def is_block_command(line):
    return any(line.startswith(cmd) for cmd in BLOCK_COMMANDS)

check_updates()

print("------------------------------------------")
print(" OlChikiLang 1.0.0 [Disom Labs] ")
print(" Olchiki Programming Language ")
print(" Commands: ᱵᱷᱟᱨᱥᱚᱱ, ᱥᱟᱯᱷᱟ, ᱜᱚᱡ, ᱛᱚᱣᱟ ")
print("------------------------------------------")


while True:
    try:

        user_input = input("ᱦᱟᱸᱥᱫᱟ >>> ").strip()

        if not user_input:
            continue


        # EXIT
        if user_input == "ᱛᱚᱣᱟ":
            print("Exiting...")
            break


        # IF BLOCK
        if is_block_command(user_input):

            block = []
            block.append(user_input)

            while True:
                line = input("    ").strip()

                if line == BLOCK_END:
                    break

                if line:
                    block.append(line)


            # execute block
            for command in block:
                parse_lines(command)

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



        # NORMAL COMMAND + DIRECT EXPRESSION
        if user_input.startswith(
            ("ᱥᱮᱴ", "ᱪᱟᱯᱟ", "ᱵᱷᱟᱨᱥᱚᱱ", "ᱥᱟᱯᱷᱟ", "ᱜᱚᱡ")
        ):
            parse_lines(user_input)

        else:
            # Python style REPL expression
            parse_lines("ᱪᱟᱯᱟ " + user_input)



    except KeyboardInterrupt:
        print(
            f"\n{RED}❌ Process interrupted! Type ᱛᱚᱣᱟ to quit.{RESET}"
        )


    except Exception as e:
        print(
            f"{RED}❌ Error: {e}{RESET}"
        )
