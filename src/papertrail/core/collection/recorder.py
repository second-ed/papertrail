from __future__ import annotations

from pathlib import Path
from typing import Self

import attrs
from io_adapters import IoAdapter, RealAdapter

from papertrail.adapters.io_funcs import FileType
from papertrail.core.collection.record import ExampleRecord


@attrs.define
class Recorder:
    path: str | Path = "./.papertrail_cache/examples.json"
    records: list[ExampleRecord] = attrs.field(factory=list)
    adapter: IoAdapter = attrs.field(factory=RealAdapter)
    files: dict = attrs.field(factory=dict)

    def __attrs_post_init__(self) -> None:
        self.path = Path(self.path)

    def record_example(self, example: ExampleRecord) -> Self:
        self.records.append(example)
        return self

    def prepare_files(self) -> Self:
        self.files[(self.path, FileType.JSON)] = [r.to_dict() for r in self.records]
        self.files[(self.path.parent / ".gitignore", FileType.STR)] = (
            "# automatically created by papertrail\n*"
        )
        return self

    def write_examples(self) -> Self:
        for k, data in self.files.items():
            path, file_type = k
            self.adapter.write(data, path, file_type)
        return self


_RECORDER = Recorder()
