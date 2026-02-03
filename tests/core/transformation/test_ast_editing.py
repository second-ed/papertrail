import pytest

from papertrail.core.transformation.ast_editing import update_function_docstrings

CODE = "\n".join(  # noqa: FLY002
    [
        "def func_a(a: float, b: float) -> float:",
        "    return a + b",
        "",
        "",
        "def func_b(a: float, b: float) -> float:",
        '    """Simple docstring',
        "",
        "    Args:",
        "        a (float)",
        "        b (float)",
        "",
        "    Returns:",
        "        float",
        '    """',
        "    return a - b",
    ]
)


EXAMPLES_1 = {
    "func_a": "Papertrail examples:\n\n    >>> func_a(2, 2) == 4\n    True\n\n    >>> func_a(2, b=3) == 5\n    True\n\n    >>> func_a(a=3, b=3) == 6\n    True\n::",
    "func_b": "Papertrail examples:\n\n    >>> func_b(2, 2) == 0\n    True\n\n    >>> func_b(2, b=3) == -1\n    True\n::",
}

EXAMPLES_2 = {
    "func_a": "Papertrail examples:\n\n    >>> func_a(5, 5) == 10\n    True\n::",
    "func_b": "Papertrail examples:\n\n    >>> func_b(3, 4) == -1\n    True\n::",
}


CODE_WITH_EXAMPLES_1 = "\n".join(  # noqa: FLY002
    [
        "def func_a(a: float, b: float) -> float:",
        '    """Papertrail examples:',
        "",
        "        >>> func_a(2, 2) == 4",
        "        True",
        "",
        "        >>> func_a(2, b=3) == 5",
        "        True",
        "",
        "        >>> func_a(a=3, b=3) == 6",
        "        True",
        "    ::",
        '    """',
        "    return a + b",
        "",
        "",
        "def func_b(a: float, b: float) -> float:",
        '    """Simple docstring',
        "",
        "    Args:",
        "        a (float)",
        "        b (float)",
        "",
        "    Returns:",
        "        float",
        "",
        "    Papertrail examples:",
        "",
        "        >>> func_b(2, 2) == 0",
        "        True",
        "",
        "        >>> func_b(2, b=3) == -1",
        "        True",
        "    ::",
        '    """',
        "    return a - b",
    ]
).strip()


CODE_WITH_EXAMPLES_2 = "\n".join(  # noqa: FLY002
    [
        "def func_a(a: float, b: float) -> float:",
        '    """Papertrail examples:',
        "",
        "        >>> func_a(5, 5) == 10",
        "        True",
        "    ::",
        '    """',
        "    return a + b",
        "",
        "",
        "def func_b(a: float, b: float) -> float:",
        '    """Simple docstring',
        "",
        "    Args:",
        "        a (float)",
        "        b (float)",
        "",
        "    Returns:",
        "        float",
        "",
        "    Papertrail examples:",
        "",
        "        >>> func_b(3, 4) == -1",
        "        True",
        "    ::",
        '    """',
        "    return a - b",
    ]
).strip()


@pytest.mark.parametrize(
    ("code", "examples", "expected_result"),
    [
        pytest.param(
            CODE, EXAMPLES_1, CODE_WITH_EXAMPLES_1, id="Ensure adds docstrings to simple functions"
        ),
        pytest.param(
            CODE_WITH_EXAMPLES_1,
            EXAMPLES_1,
            CODE_WITH_EXAMPLES_1,
            id="Ensure leaves the docstrings unchanged if they already have examples",
        ),
        pytest.param(
            CODE_WITH_EXAMPLES_1,
            EXAMPLES_2,
            CODE_WITH_EXAMPLES_2,
            id="Ensure updates the docstrings if they have new examples",
        ),
    ],
)
def test_update_function_docstrings(code, examples, expected_result):
    assert update_function_docstrings(code, examples) == expected_result
