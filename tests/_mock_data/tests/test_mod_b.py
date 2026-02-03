import string

import pytest
from mock_src.mod_b import enum_keys

from papertrail import example


@pytest.mark.parametrize(
    ("args", "kwargs", "expected_result"),
    [
        pytest.param(
            (dict(enumerate(string.ascii_lowercase[:5])),),
            {},
            [
                "",
                "b",
                "cc",
                "ddd",
                "eeee",
            ],
        ),
    ],
)
def test_enum_keys(args, kwargs, expected_result):
    assert example(enum_keys, *args, **kwargs) == expected_result
