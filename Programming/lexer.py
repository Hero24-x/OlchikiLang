# -*- coding: utf-8 -*-

# =========================
# TOKEN
# =========================

class Token:

    def __init__(self, type_, value, line, col):

        self.type = type_
        self.value = value

        self.line = line
        self.col = col

    def __repr__(self):

        return (
            f"Token("
            f"type={self.type}, "
            f"value={self.value}, "
            f"line={self.line}, "
            f"col={self.col}"
            f")"
        )


# =========================
# LEXER ERROR
# =========================

class LexerError(Exception):

    pass


# =========================
# OLCHIKI DIGITS
# =========================

OLCHIKI_DIGITS = {
    "᱐": "0",
    "᱑": "1",
    "᱒": "2",
    "᱓": "3",
    "᱔": "4",
    "᱕": "5",
    "᱖": "6",
    "᱗": "7",
    "᱘": "8",
    "᱙": "9"
}


# =========================
# KEYWORDS
# =========================

KEYWORDS = {

    "ᱪᱟᱯᱟ": "PRINT",
    "ᱥᱮᱴ": "SET",

    "ᱯᱩᱱ": "FUNCTION",
    "ᱫᱟᱨ": "RETURN",

    "ᱡᱩᱫᱤ": "IF",
    "ᱮᱞᱥᱮ": "ELSE",

    "ᱫᱚᱦᱚᱨ": "LOOP",

    "ᱢᱟᱨᱟ": "VAR"
}


# =========================
# SYMBOLS
# =========================

SYMBOLS = {

    "+": "PLUS",
    "-": "MINUS",

    "*": "MUL",
    "/": "DIV",

    "=": "ASSIGN",

    "(": "LPAREN",
    ")": "RPAREN",

    "{": "LBRACE",
    "}": "RBRACE",

    ",": "COMMA"
}


# =========================
# HELPERS
# =========================

def convert_olchiki_number(text):

    result = ""

    for ch in text:

        if ch in OLCHIKI_DIGITS:
            result += OLCHIKI_DIGITS[ch]
        else:
            result += ch

    return result


def make_identifier_token(text, line, col):

    if text in KEYWORDS:

        return Token(
            KEYWORDS[text],
            text,
            line,
            col
        )

    return Token(
        "IDENTIFIER",
        text,
        line,
        col
    )


# =========================
# MAIN TOKENIZER
# =========================

def tokenize(source_code):

    tokens = []

    i = 0

    line = 1
    col = 1

    while i < len(source_code):

        ch = source_code[i]

        # =====================
        # NEWLINE
        # =====================

        if ch == "\n":

            line += 1
            col = 1

            i += 1
            continue

        # =====================
        # WHITESPACE
        # =====================

        if ch in " \t\r":

            i += 1
            col += 1
            continue

        # =====================
        # STRING
        # =====================

        if ch == '"':

            start_col = col

            i += 1
            col += 1

            value = ""

            while i < len(source_code):

                current = source_code[i]

                if current == '"':
                    break

                value += current

                i += 1
                col += 1

            else:

                raise LexerError(
                    f"Unclosed string at line {line}"
                )

            tokens.append(
                Token(
                    "STRING",
                    value,
                    line,
                    start_col
                )
            )

            i += 1
            col += 1

            continue

        # =====================
        # NUMBER
        # =====================

        if ch in OLCHIKI_DIGITS:

            start_col = col

            value = ""

            while (
                i < len(source_code)
                and source_code[i] in OLCHIKI_DIGITS
            ):

                value += source_code[i]

                i += 1
                col += 1

            value = convert_olchiki_number(value)

            tokens.append(
                Token(
                    "NUMBER",
                    int(value),
                    line,
                    start_col
                )
            )

            continue

        # =====================
        # IDENTIFIER / KEYWORD
        # =====================

        if ch.isalpha() or ord(ch) >= 0x1C50:

            start_col = col

            value = ""

            while (
                i < len(source_code)
                and (
                    source_code[i].isalnum()
                    or ord(source_code[i]) >= 0x1C50
                    or source_code[i] == "_"
                )
            ):

                value += source_code[i]

                i += 1
                col += 1

            tokens.append(
                make_identifier_token(
                    value,
                    line,
                    start_col
                )
            )

            continue

        # =====================
        # SYMBOLS
        # =====================

        if ch in SYMBOLS:

            tokens.append(
                Token(
                    SYMBOLS[ch],
                    ch,
                    line,
                    col
                )
            )

            i += 1
            col += 1

            continue

        # =====================
        # UNKNOWN CHARACTER
        # =====================

        raise LexerError(
            f"Unknown character '{ch}' "
            f"at line {line}, col {col}"
        )

    return tokens
