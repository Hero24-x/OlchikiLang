# spl/lexer.py
import os
import re

def tokenize(line):
    # 🔥 Fix: Ol Chiki digits mapping corrected (0-9 standard unicode)
    olchiki_digits = {
        "᱐":"0", "᱑":"1", "᱒":"2", "᱓":"3", "᱔":"4",
        "᱕":"5", "᱖":"6", "᱗":"7", "᱘":"8", "᱙":"9"
    }

    # 🔥 V2 FEATURE: Single-line Comment Support (#)
    # Agar line mein '#' hai, toh uske baad ka hissa hata do
    if "#" in line:
        line = line.split("#")[0]

    clean_line = line.strip()
    if not clean_line:
        return []

    # Poori line ke Ol Chiki digits ko ASCII digits me replace karein
    for k, v in olchiki_digits.items():
        clean_line = clean_line.replace(k, v)

    # Space splitting se primary chunks nikalein
    initial_chunks = clean_line.split()
    result = []

    # Har chunk se operators (+, -, *, /, (, )) alag karein
    for token in initial_chunks:
        if any(op in token for op in "+-*_=,/\<>{}[],()"):
            temp = ""
            for ch in token:
                if ch in "+-*_=,/\<>[]{}()":
                    if temp:
                        result.append(temp)
                        temp = ""
                    result.append(ch)
                else:
                    temp += ch
            if temp:
                result.append(temp)
        else:
            result.append(token)

    return result
