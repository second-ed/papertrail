from __future__ import annotations

from collections.abc import Generator
from typing import Any

import pytest
from _pytest.config import ExitCode
from _pytest.main import Session

from papertrail.adapters.io_funcs import FileType
from papertrail.core.collection.recorder import _RECORDER
from papertrail.core.transformation.transform import update_modified_docstrings


@pytest.hookimpl(hookwrapper=True, trylast=True)
def pytest_sessionfinish(
    session: Session,  # noqa: ARG001
    exitstatus: int | ExitCode,  # noqa: ARG001
) -> Generator[Any, None, None]:
    yield

    _RECORDER.prepare_files().write_examples()
    update_modified_docstrings(
        _RECORDER.adapter, _RECORDER.adapter.read(_RECORDER.path, FileType.JSON)
    )
