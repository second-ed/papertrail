import json
from enum import Enum, unique
from pathlib import Path
from typing import Any

from io_adapters import register_read_fn, register_write_fn


@unique
class FileType(Enum):
    STR = "str"
    JSON = "json"


@register_read_fn(FileType.STR)
def read_str(path: str, **kwargs: dict[str, Any]) -> str:
    return Path(path).read_text(**kwargs)


@register_write_fn(FileType.STR)
def write_str(data: str, path: str, **kwargs: dict[str, Any]) -> None:
    _make_dirs(path).write_text(data, **kwargs)


@register_read_fn(FileType.JSON)
def read_json(path: str, **kwargs: dict[str, Any]) -> dict:
    return json.safe_load(Path(path).read_text(), **kwargs)


@register_write_fn(FileType.JSON)
def write_json(data: str, path: str, **kwargs: dict[str, Any]) -> None:
    _make_dirs(path).write_text(json.dumps(data, indent=2, sort_keys=False, **kwargs))


def _make_dirs(path: str) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    return path
