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
                str(Path(inspect.getsourcefile(self.fn))),
                str(self.args),
                str(self.kwargs),
                self.value,
            ]
        )
        return hash(hash_value)


def example(fn: Callable, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> Example:
    value = fn(*args, **kwargs)
    return Example(fn, args, kwargs, value, recorder=_RECORDER)
