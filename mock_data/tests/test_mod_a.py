import pytest
from mock_src.mod_a import func_a

from papertrail import example


@pytest.mark.parametrize(
    ("a", "b", "expected_result"), [pytest.param(2, 2, 4), pytest.param(2, 3, 5)]
)
def test_func_a(a, b, expected_result):
    assert example(func_a, a, b) == expected_result
