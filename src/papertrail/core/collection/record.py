from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True, slots=True, eq=True)
class ExampleRecord:
    fn_name: str
    module: str
    src_file: str
    src_line: int
    args: tuple[Any, ...]
    kwargs: dict[str, Any]
    returned: Any
    expected: Any

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
