
import ast

with open('app.py', 'r', encoding='utf-8') as f:
    try:
        ast.parse(f.read())
        print("SUCCESS")
    except SyntaxError as e:
        print(f"SYNTAX ERROR: {e}")
        print(f"Line: {e.lineno}")
        print(f"Offset: {e.offset}")
        print(f"Text: {e.text}")
