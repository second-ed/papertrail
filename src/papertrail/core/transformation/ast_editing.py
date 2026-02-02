import ast
import re
from typing import Self

import attrs


def update_function_docstrings(code: str, examples: dict[str, str]) -> str:
    replacements = create_replacements(code, examples)
    return replace_docstrings(code, replacements)


@attrs.define(frozen=True)
class DocString:
    doc: str
    start_line: int
    end_line: int
    indent: str = "    "

    @classmethod
    def from_doc_node(cls, node: ast.AST) -> Self:
        return cls(node.value.value.rstrip(), node.lineno - 1, node.end_lineno)

    @classmethod
    def from_non_doc_node(cls, node: ast.AST) -> Self:
        start = node.lineno - 1
        return cls("", start, start)

    def with_example(self, example: str) -> Self:
        example = "".join(
            [
                f"{self.indent}{line}" if line.strip() else line
                for line in example.splitlines(keepends=True)
            ]
        )
        pattern = r"(?ms)^[ \t]*Papertrail examples:\n.*?\n[ \t]*::"
        replaced_doc, n = re.subn(pattern, example, self.doc)

        new_doc = replaced_doc if n else f"{self.doc}\n\n{example}"
        return DocString(new_doc.strip(), self.start_line, self.end_line)

    def to_doc(self) -> str:
        return f'{self.indent}"""{self.doc.strip()}\n{self.indent}"""\n'


def create_replacements(code: str, examples: dict[str, str]) -> list[DocString]:
    tree = ast.parse(code)

    replacements = []

    for node in ast.walk(tree):
        if not _is_fn_with_body(node) or not (example := examples.get(node.name, "")):
            continue

        first = node.body[0]

        if _is_docstring(first):
            docstring = DocString.from_doc_node(first)
        else:
            docstring = DocString.from_non_doc_node(first)

        replacements.append(docstring.with_example(example))

    return replacements


def replace_docstrings(code: str, replacements: list[DocString]) -> str:
    lines = code.splitlines(keepends=True)
    for doc in reversed(replacements):
        lines[doc.start_line : doc.end_line] = [doc.to_doc()]

    return "".join(lines)


def _is_fn_with_body(node: ast.AST) -> bool:
    return isinstance(node, ast.FunctionDef) and node.body


def _is_docstring(node: ast.AST) -> bool:
    return (
        isinstance(node, ast.Expr)
        and isinstance(node.value, ast.Constant)
        and isinstance(node.value.value, str)
    )
