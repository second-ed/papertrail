import ast

import black


def update_function_docstrings(
    code: str,
    examples: dict[str, str],
) -> str:
    lines = code.splitlines(keepends=True)
    tree = ast.parse(code)

    replacements: list[tuple[int, int, str]] = []

    for node in ast.walk(tree):
        if is_fn_with_body(node) or not (example := examples.get(node.name)):
            continue

        first = node.body[0]
        start = first.lineno - 1
        indent = " " * (first.col_offset)

        if is_docstring(first):
            new_doc = f"{first.value.value.rstrip()}\n\n{example}\n"
            quoted = f'{indent}"""{new_doc}{indent}"""\n'
            replacements.append((start, first.end_lineno, quoted))
        else:
            new_docstring = f'{indent}"""{example}\n{indent}"""\n'
            replacements.append((start, start, new_docstring))

    for start, end, text in reversed(replacements):
        lines[start:end] = [text]

    return black.format_str("".join(lines), mode=black.FileMode()).strip()


def is_fn_with_body(node: ast.AST) -> bool:
    return not isinstance(node, ast.FunctionDef) or not node.body


def is_docstring(node: ast.AST) -> bool:
    return (
        isinstance(node, ast.Expr)
        and isinstance(node.value, ast.Constant)
        and isinstance(node.value.value, str)
    )
