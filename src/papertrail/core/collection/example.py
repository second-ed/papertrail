"""repo-map-desc: User entrypoint `example` and it's inner class `Example`

The equality operator is where the magic happens
"""

from __future__ import annotations

import inspect
from collections.abc import Callable
from pathlib import Path
from typing import Any, TypeVar

import attrs

from papertrail.core.collection.record import ExampleRecord
from papertrail.core.collection.recorder import _RECORDER, Recorder

T = TypeVar("T")


@attrs.define
class Example:
    fn: Callable
    args: tuple[Any, ...]
    kwargs: dict[str, Any]
    value: Any
    recorder: Recorder

    def __eq__(self, expected: T) -> bool:
        record = ExampleRecord(
            fn_name=self.fn.__name__,
            module=self.fn.__module__,
            src_file=str(Path(inspect.getsourcefile(self.fn))),
            args=self.args,
            kwargs=self.kwargs,
            returned=self.value,
            expected=expected,
        )

        self.recorder.record_example(record)
        return self.value == expected

    def __hash__(self) -> int:
        hash_value = "".join(
            [
                self.fn.__name__,
                self.fn.__module__,
                str(self.args),
                str(self.kwargs),
                str(self.value),
            ]
        )
        return hash(hash_value)


def example(fn: Callable, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> Example:
    """Capture an example from a test to add to the docstring.

    Wrap the example around the function before the equality operation and the function result will be captured and added to the docstring of the function.
    This only happens if the tests pass!

    .. code-block:: python

        from papertrail import example

        def test_add():
            assert example(add, 2, 3) == 5


    This has captured the example and now once the tests are finished the docstring of the function will be updated like this:

    .. code-block:: python

        def add(a: int, b: int) -> int:
            \"\"\"Papertrail examples:

                >>> add(2, 3) == 5
                True
            ::
            \"\"\"
            return a + b


    You can use it with parametrized tests too:

    .. code-block:: python

        @pytest.mark.parametrize(
            ("args", "kwargs", "expected_result"),
            [
                pytest.param((2, 2), {}, 0),
                pytest.param((2,), {"b": 3}, -1),
            ],
        )
        def test_func_b(args, kwargs, expected_result):
            assert example(func_b, *args, **kwargs) == expected_result

    This captures all the cases and adds them to the functions docstring:

    .. code-block:: python

        def func_b(a: float, b: float) -> float:
            \"\"\"Simple docstring

            Args:
                a (float)
                b (float)

            Returns:
                float

            Papertrail examples:

                >>> func_b(3, 4) == -1
                True
            ::
            \"\"\"
            return a - b
    """
    value = fn(*args, **kwargs)
    return Example(fn, args, kwargs, value, recorder=_RECORDER)
