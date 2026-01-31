from __future__ import annotations

import inspect
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any, TypeVar

from papertrail.core.collection.record import ExampleRecord
from papertrail.core.collection.recorder import _RECORDER, Recorder

T = TypeVar("T")


@dataclass(slots=True)
class Example:
    fn: Callable
    args: tuple[Any, ...]
    kwargs: dict[str, Any]
    value: Any
    recorder: Recorder

    def __eq__(self, expected: T) -> bool:
        frame = inspect.currentframe().f_back

        record = ExampleRecord(
            fn_name=self.fn.__name__,
            module=self.fn.__module__,
            src_file=str(Path(inspect.getsourcefile(self.fn))),
            src_line=frame.f_lineno,
            args=self.args,
            kwargs=self.kwargs,
            returned=self.value,
            expected=expected,
        )

        self.recorder.record_example(record)
        return self.value == expected


def example(fn: Callable, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> Example:
    value = fn(*args, **kwargs)
    return Example(fn, args, kwargs, value, recorder=_RECORDER)
