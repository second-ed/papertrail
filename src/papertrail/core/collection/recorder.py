from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Self

from io_adapters import IoAdapter, RealAdapter

from papertrail.adapters.io_funcs import FileType
from papertrail.core.collection.record import ExampleRecord


@dataclass(slots=True)
class Recorder:
    path: str | Path = "./.papertrail_cache/examples.json"
    records: list[ExampleRecord] = field(default_factory=list)
    adapter: IoAdapter = field(default_factory=RealAdapter)
    files: dict = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.path = Path(self.path)

    def record_example(self, example: ExampleRecord) -> Self:
        self.records.append(example)
        return self

    def prepare_files(self) -> Self:
        self.files[(self.path, FileType.JSON)] = [r.to_dict() for r in self.records]
        self.files[(self.path.parent.joinpath(".gitignore"), FileType.STR)] = (
            "# automatically created by papertrail\n*"
        )
        return self

    def write_examples(self) -> Self:
        for k, data in self.files.items():
            path, file_type = k
            self.adapter.write(data, path, file_type)
        return self


_RECORDER = Recorder()
