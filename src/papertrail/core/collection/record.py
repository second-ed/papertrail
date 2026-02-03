from __future__ import annotations

from typing import Any

import attrs


@attrs.define(frozen=True, eq=True)
class ExampleRecord:
    fn_name: str
    module: str
    src_file: str
    args: tuple[Any, ...]
    kwargs: dict[str, Any]
    returned: Any
    expected: Any

    def to_dict(self) -> dict[str, str]:
        return attrs.asdict(self)
