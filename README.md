# papertrail

### Motivation
- Documentation can get out of date quickly
- Sometimes its harder to explain what a function does in plain english than it is to just show what the input and outputs would be:
    - e.g:
        - "Multiply the value strings by the amount that is the key".
    - vs
        - `f({"a": 1, "b": 2, "c": 4}) == ['a', 'bb', 'cccc']`
- Tests are the best form of documentation because they complain when they go out of sync
- Doctests are an interesting way of writing tests however they can be fiddly and harder to set up than proper testing frameworks
- Resorting to only using doctests means missing out on features like fixtures and parameterisation
- Having some tests that are written in tests and some that are in doctests means keeping track of two places as the "source of truth"

### Installation
```shell
uv add papertrail
```

### Example
Use the `example` function to capture an example from a test to add to the docstring.

Wrap the example around the function before the equality operation and the function result will be captured and added to the docstring of the function.
This only happens if the tests pass!

```python
from papertrail import example

def test_add():
    assert example(add, 2, 3) == 5
```

This has captured the example and now once the tests are finished the docstring of the function will be updated like this:

```python
def add(a: int, b: int) -> int:
    """Papertrail examples:

        >>> add(2, 3) == 5
        True
    ::
    """
    return a + b
```

You can use it with parametrized tests too:

```python
@pytest.mark.parametrize(
    ("args", "kwargs", "expected_result"),
    [
        pytest.param((2, 2), {}, 0),
        pytest.param((2,), {"b": 3}, -1),
    ],
)
def test_func_b(args, kwargs, expected_result):
    assert example(func_b, *args, **kwargs) == expected_result
```

This captures all the cases and adds them to the functions docstring:

```python
def func_b(a: float, b: float) -> float:
    """Simple docstring

    Args:
        a (float)
        b (float)

    Returns:
        float

    Papertrail examples:

        >>> func_b(2, 2) == 0
        True

        >>> func_b(2, b=3) == -1
        True
    ::
    """
    return a - b
```

# Repo map
```
├── .github
│   └── workflows
│       ├── ci_tests.yaml
│       └── publish.yaml
├── src
│   └── papertrail
│       ├── adapters
│       │   ├── __init__.py
│       │   └── io_funcs.py              # The IO functions for the IO adapters
│       ├── core
│       │   ├── collection
│       │   │   ├── __init__.py
│       │   │   ├── example.py           # User entrypoint `example` and it's inner class `Example`
│       │   │   ├── record.py
│       │   │   └── recorder.py
│       │   ├── transformation
│       │   │   ├── __init__.py
│       │   │   ├── ast_editing.py
│       │   │   ├── format_examples.py
│       │   │   └── transform.py         # Updates the the docstrings for all the funcs in the files in the example cache.
│       │   ├── __init__.py
│       │   └── logger.py
│       ├── __init__.py
│       └── __main__.py                  # the pytest hook for sessionfinish
├── tests
│   ├── _mock_data
│   │   ├── mock_src
│   │   │   ├── __init__.py
│   │   │   ├── mod_a.py
│   │   │   └── mod_b.py
│   │   └── tests
│   │       ├── __init__.py
│   │       ├── conftest.py
│   │       ├── test_mod_a.py
│   │       └── test_mod_b.py
│   ├── core
│   │   ├── collection
│   │   │   ├── __init__.py
│   │   │   ├── test_example.py
│   │   │   ├── test_record.py
│   │   │   └── test_recorder.py
│   │   └── transformation
│   │       ├── __init__.py
│   │       ├── test_ast_editing.py
│   │       └── test_format_examples.py
│   └── test_main.py
├── .pre-commit-config.yaml
├── README.md
├── pyproject.toml
├── ruff.toml
└── uv.lock

(generated with repo-mapper-rs)
::
```
