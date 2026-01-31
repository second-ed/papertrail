import pytest
from mock_src.mod_a import func_a, func_b

from papertrail import example


@pytest.mark.parametrize(
    ("args", "kwargs", "expected_result"),
    [
        pytest.param((2, 2), {}, 4),
        pytest.param((2,), {"b": 3}, 5),
        pytest.param((), {"a": 3, "b": 3}, 6),
    ],
)
def test_func_a(args, kwargs, expected_result):
    assert example(func_a, *args, **kwargs) == expected_result


@pytest.mark.parametrize(
    ("args", "kwargs", "expected_result"),
    [
        pytest.param((2, 2), {}, 0),
        pytest.param((2,), {"b": 3}, -1),
    ],
)
def test_func_b(args, kwargs, expected_result):
    assert example(func_b, *args, **kwargs) == expected_result
