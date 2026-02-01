from __future__ import annotations

from collections.abc import Generator
from typing import Any

import pytest
from _pytest.config import ExitCode
from _pytest.main import Session

from papertrail.core.collection.recorder import _RECORDER, Recorder
from papertrail.core.transformation.transform import update_modified_docstrings


@pytest.hookimpl(hookwrapper=True, trylast=True)
def pytest_sessionfinish(
    session: Session,  # noqa: ARG001
    exitstatus: int | ExitCode,  # noqa: ARG001
) -> Generator[Any, None, None]:
    yield
    main(_RECORDER)


def main(recorder: Recorder) -> None:
    recorder.prepare_files().write_examples()
    update_modified_docstrings(recorder.adapter, recorder.path)
