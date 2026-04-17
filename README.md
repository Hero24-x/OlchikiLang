#OlchikiLang

**OlchikiLang** is an experimental programming language built using the **Ol Chiki script** used for the Santali language.

The goal of this project is to demonstrate that programming languages do not need to rely on Latin scripts.
OlchikiLang explores how a full programming language can be designed using an indigenous writing system.

To the best of our knowledge, **OlchikiLang is the first programming language created using the Ol Chiki script for Santali**.

---

## 🌍 Vision

Most programming languages in the world use the **Latin alphabet** for syntax and keywords.
OlchikiLang explores a different idea:

👉 Programming using the **Ol Chiki writing system**

This project aims to promote:

* Indigenous language technology
* Programming accessibility for Santali speakers
* Experimental language design

---

## ⚡ Features

Current features of OlchikiLang include:

* 🔢 Ol Chiki number system support
* ➕ Arithmetic expressions
* 📦 Variables
* 🔁 Loops
* 🔀 Conditional statements
* 🖥 Interactive REPL interpreter

Example supported operations:

* Addition
* Subtraction
* Multiplication
* Division

---

## 🧠 Example Code

Example OlchikiLang program:

```
ᱪᱟᱯᱟ (᱑ + ᱒ + ᱓) * (᱒ + ᱑)
```

Output:

```
᱑᱘
```

Another example:

```
ᱥᱮᱴ x ᱕
ᱪᱟᱯᱟ x
```

Output:

```
᱕
```

---

## 🏗 Architecture

OlchikiLang follows a simple compiler/interpreter architecture:

```
Source Code
   ↓
Lexer (Tokenization)
   ↓
Parser (AST Creation)
   ↓
AST Nodes
   ↓
Virtual Machine / Interpreter
   ↓
Output
```

Project structure:

```
OlchikiLang/
│
├── lexer.py
├── parser.py
├── ast_nodes.py
├── vm.py
├── compiler.py
├── interpreter.py
├── run.py
├── program.olc
└── README.md
```

---

## ▶ Running the Language

Start the interpreter:

```
python run.py
```

Interactive mode:

```
ᱦᱟᱸᱥᱫᱟ >>>
```

Exit command:

```
ᱟᱹᱠᱥᱤᱴ
```

---

## 🔮 Future Plans

Planned improvements:

* Functions
* File execution support
* Package system
* Better error messages
* IDE syntax highlighting
* Compiler mode

---

## 🤝 Contributing

This is an experimental open-source project.
Contributions, improvements, and research ideas are welcome.

---

## 📜 License

Open Source Project

---

## 👨‍💻 Author

**Shibnath Hansda**

Creator of **OlchikiLang**
🧠 First experimental **Ol-Chiki Santali Programming Language**

🔗 GitHub: https://github.com/Hero24-x

## License

This project is licensed under the GNU GPL v3.0 License.

© 2026 Shibnath Hansda
