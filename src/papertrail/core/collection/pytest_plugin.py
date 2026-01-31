from __future__ import annotations

from collections.abc import Generator
from typing import Any

import pytest
from _pytest.config import ExitCode
from _pytest.main import Session

from papertrail.core.collection.recorder import _RECORDER


@pytest.hookimpl(hookwrapper=True, trylast=True)
def pytest_sessionfinish(
    session: Session,  # noqa: ARG001
    exitstatus: int | ExitCode,  # noqa: ARG001
) -> Generator[Any, None, None]:
    yield

    _RECORDER.prepare_files().write_examples()
