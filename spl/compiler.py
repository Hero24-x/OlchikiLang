from spl.lexer import tokenize
# parser.py ke sahi function names ko import kiya 👇
from spl.parser import parse_line, parse_lines 

# Single line ko tokens me tod kar node banane ke liye
def compile_line(line):
    # Lexer se tokens nikalna (jo aapne abhi fix kiya)
    tokens_list = tokenize(line)
    
    # Parser ko tokens ki list pass karne ke bajay pure string pass karein,
    # kyunki hamara updated parser andar khud tokenize karta hai.
    node = parse_line(line)
    return node

# Full program code (Multi-line) ko ek sath AST me badalne ke liye
def compile_program(code_string):
    """
    Pore program ko array of lines me convert karke
    iska ek full Abstract Syntax Tree (AST) return karega.
    """
    lines = code_string.split("\n")
    ast = parse_lines(lines)
    return ast
