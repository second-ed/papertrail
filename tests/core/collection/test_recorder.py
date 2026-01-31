import pytest
from io_adapters import FakeAdapter

from papertrail.core.collection.record import ExampleRecord
from papertrail.core.collection.recorder import Recorder


@pytest.mark.parametrize(
    ("record", "expected_result"),
    [
        pytest.param(
            ExampleRecord(
                fn_name="func_a",
                module="src.mod_a",
                src_file="mock_data/src/mod_a.py",
                args=[2, 2],
                kwargs={},
                returned=4,
                expected=4,
            ),
            {
                ".papertrail_cache/.gitignore": "# automatically created by papertrail\n*",
                ".papertrail_cache/examples.json": [
                    {
                        "args": [
                            2,
                            2,
                        ],
                        "expected": 4,
                        "fn_name": "func_a",
                        "kwargs": {},
                        "module": "src.mod_a",
                        "returned": 4,
                        "src_file": "mock_data/src/mod_a.py",
                    },
                ],
            },
        )
    ],
)
def test_recorder(record, expected_result):
    adapter = FakeAdapter()
    recorder = Recorder(adapter=adapter)
    recorder.record_example(record).prepare_files().write_examples()
    assert adapter.files == expected_result
