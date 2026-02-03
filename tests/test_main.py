"""Faked E2E test."""  # noqa: INP001

import pytest
from _mock_data.mock_src.mod_a import func_a, func_b
from io_adapters import FakeAdapter

from papertrail.__main__ import main
from papertrail.core.collection.example import Example
from papertrail.core.collection.recorder import Recorder
from papertrail.core.logger import REPO_ROOT

STARTING_FILES_1 = {
    f"{REPO_ROOT}/tests/_mock_data/mock_src/mod_a.py": "\n".join(  # noqa: FLY002
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
}

CONFIG_1 = (
    (func_a, (2, 2), {}, 4),
    (func_a, (2,), {"b": 3}, 5),
    (func_a, (), {"a": 3, "b": 3}, 6),
    (func_b, (2, 2), {}, 0),
    (func_b, (2,), {"b": 3}, -1),
)


EXPECTED_RESULT_1 = {
    ".papertrail_cache/examples.json": [
        {
            "args": (2, 2),
            "expected": 4,
            "fn_name": "func_a",
            "kwargs": {},
            "module": "_mock_data.mock_src.mod_a",
            "returned": 4,
            "src_file": f"{REPO_ROOT}/tests/_mock_data/mock_src/mod_a.py",
        },
        {
            "args": (2,),
            "expected": 5,
            "fn_name": "func_a",
            "kwargs": {"b": 3},
            "module": "_mock_data.mock_src.mod_a",
            "returned": 5,
            "src_file": f"{REPO_ROOT}/tests/_mock_data/mock_src/mod_a.py",
        },
        {
            "args": (),
            "expected": 6,
            "fn_name": "func_a",
            "kwargs": {"a": 3, "b": 3},
            "module": "_mock_data.mock_src.mod_a",
            "returned": 6,
            "src_file": f"{REPO_ROOT}/tests/_mock_data/mock_src/mod_a.py",
        },
        {
            "args": (2, 2),
            "expected": 0,
            "fn_name": "func_b",
            "kwargs": {},
            "module": "_mock_data.mock_src.mod_a",
            "returned": 0,
            "src_file": f"{REPO_ROOT}/tests/_mock_data/mock_src/mod_a.py",
        },
        {
            "args": (2,),
            "expected": -1,
            "fn_name": "func_b",
            "kwargs": {"b": 3},
            "module": "_mock_data.mock_src.mod_a",
            "returned": -1,
            "src_file": f"{REPO_ROOT}/tests/_mock_data/mock_src/mod_a.py",
        },
    ],
    f"{REPO_ROOT}/tests/_mock_data/mock_src/mod_a.py": "\n".join(  # noqa: FLY002
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
    ),
}


@pytest.mark.parametrize(
    ("files", "config", "expected_files"),
    [
        pytest.param(
            STARTING_FILES_1, CONFIG_1, EXPECTED_RESULT_1, id="E2E test with simple functions"
        )
    ],
)
def test_main(files, config, expected_files):
    adapter = FakeAdapter(files=files)
    recorder = Recorder(adapter=adapter)

    for fn, args, kwargs, expected_result in config:
        value = fn(*args, **kwargs)
        _ = Example(fn, args, kwargs, value=value, recorder=recorder) == expected_result

    main(recorder)
    assert adapter.files == {
        ".papertrail_cache/.gitignore": "# automatically created by papertrail\n*",
        **expected_files,
    }
