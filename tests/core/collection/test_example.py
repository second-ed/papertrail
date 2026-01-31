import pytest
from io_adapters import FakeAdapter

from papertrail.core import REPO_ROOT
from papertrail.core.collection import Example, Recorder


def mock_fn(a: int, b: int) -> int:
    return a + b


@pytest.mark.parametrize(
    ("args", "kwargs", "expected_result"),
    [
        pytest.param(
            (2,),
            {"b": 2},
            {
                ".papertrail_cache/.gitignore": "# automatically created by papertrail\n*",
                ".papertrail_cache/examples.json": [
                    {
                        "args": (2,),
                        "expected": 4,
                        "fn_name": "mock_fn",
                        "kwargs": {
                            "b": 2,
                        },
                        "module": "collection.test_example",
                        "returned": 4,
                        "src_file": f"{REPO_ROOT}/tests/core/collection/test_example.py",
                    },
                ],
            },
        )
    ],
)
def test_example(args, kwargs, expected_result):
    adapter = FakeAdapter()
    recorder = Recorder(adapter=adapter)
    example = Example(mock_fn, args, kwargs, 4, recorder=recorder)

    # do equality op to capture the record
    _ = example == 4

    example.recorder.prepare_files().write_examples()
    assert adapter.files == expected_result


@pytest.mark.parametrize(
    ("args", "kwargs", "value"),
    [
        pytest.param((2,), {"b": 2}, 4),
        pytest.param((2, 3), {}, 5),
    ],
)
def test_example_equality(args, kwargs, value):
    adapter = FakeAdapter()
    recorder = Recorder(adapter=adapter)
    e1 = Example(mock_fn, args, kwargs, value, recorder=recorder)
    e2 = Example(mock_fn, args, kwargs, value, recorder=recorder)

    assert e1 == e2
    assert hash(e1) == hash(e2)
