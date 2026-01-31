from typing import Any

from papertrail.core.collection.recorder import _RECORDER


def pytest_sessionfinish(session: Any, exitstatus: int) -> None:  # noqa: ARG001 ANN401
    _RECORDER.write_examples()
