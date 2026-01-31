import pytest

from papertrail.core.transformation.format_examples import (
    collect_example_strs,
    reduce_examples_to_example_str,
)

MOCK_EXAMPLES = [
    {
        "fn_name": "func_a",
        "module": "mock_src.mod_a",
        "src_file": "mock_src/mod_a.py",
        "args": [2, 2],
        "kwargs": {},
        "returned": 4,
        "expected": 4,
    },
    {
        "fn_name": "func_a",
        "module": "mock_src.mod_a",
        "src_file": "mock_src/mod_a.py",
        "args": [2],
        "kwargs": {"b": 3},
        "returned": 5,
        "expected": 5,
    },
    {
        "fn_name": "func_a",
        "module": "mock_src.mod_a",
        "src_file": "mock_src/mod_a.py",
        "args": [],
        "kwargs": {"a": 3, "b": 3},
        "returned": 6,
        "expected": 6,
    },
    {
        "fn_name": "func_a",
        "module": "mock_src.mod_a",
        "src_file": "mock_src/mod_a.py",
        "args": [],
        "kwargs": {"a": 3, "b": 3},
        "returned": 6,
        "expected": 5,
    },
    {
        "fn_name": "func_b",
        "module": "mock_src.mod_a",
        "src_file": "mock_src/mod_a.py",
        "args": [3],
        "kwargs": {"b": 3},
        "returned": 6,
        "expected": 6,
    },
]


@pytest.mark.parametrize(
    ("examples", "expected_result"),
    [
        pytest.param(
            MOCK_EXAMPLES,
            {
                "mock_src/mod_a.py": {
                    "func_a": [
                        "    >>> func_a(2, 2) == 4\n    True",
                        "    >>> func_a(2, b=3) == 5\n    True",
                        "    >>> func_a(a=3, b=3) == 6\n    True",
                    ],
                    "func_b": ["    >>> func_b(3, b=3) == 6\n    True"],
                }
            },
        )
    ],
)
def test_collect_example_strs(examples, expected_result):
    assert collect_example_strs(examples) == expected_result


@pytest.mark.parametrize(
    ("examples", "expected_result"),
    [
        pytest.param(
            {
                "mock_src/mod_a.py": {
                    "func_a": [
                        "    >>> func_a(2, 2) == 4\n    True",
                        "    >>> func_a(2, b=3) == 5\n    True",
                        "    >>> func_a(a=3, b=3) == 6\n    True",
                    ],
                    "func_b": ["    >>> func_b(3, b=3) == 6\n    True"],
                }
            },
            {
                "mock_src/mod_a.py": {
                    "func_a": "Papertrail examples:\n\n    >>> func_a(2, 2) == 4\n    True\n\n    >>> func_a(2, b=3) == 5\n    True\n\n    >>> func_a(a=3, b=3) == 6\n    True\n::",
                    "func_b": "Papertrail examples:\n\n    >>> func_b(3, b=3) == 6\n    True\n::",
                }
            },
        )
    ],
)
def test_reduce_examples_to_example_str(examples, expected_result):
    assert reduce_examples_to_example_str(examples) == expected_result
