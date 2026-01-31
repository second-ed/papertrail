from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

from papertrail.core.collection.record import ExampleRecord


@dataclass(slots=True)
class Recorder:
    path: str | Path = "./.papertrail_cache/examples.json"
    records: list[ExampleRecord] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.path = Path(self.path)

    def record_example(self, example: ExampleRecord) -> None:
        self.records.append(example)

    def write_examples(self) -> None:
        records = [r.to_dict() for r in self.records]

        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.create_gitignore()
        self.path.write_text(json.dumps(records, indent=2, sort_keys=False))

    def create_gitignore(self) -> None:
        lines = "# automatically created by papertrail\n*"
        gitignore_path = self.path.parent.joinpath(".gitignore")
        gitignore_path.write_text(lines)


_RECORDER = Recorder()
