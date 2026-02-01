# papertrail


# Repo map
```
├── .github
│   └── workflows
│       └── ci_tests.yaml
├── src
│   └── papertrail
│       ├── adapters
│       │   ├── __init__.py
│       │   └── io_funcs.py
│       ├── core
│       │   ├── collection
│       │   │   ├── __init__.py
│       │   │   ├── example.py
│       │   │   ├── record.py
│       │   │   └── recorder.py
│       │   ├── transformation
│       │   │   ├── __init__.py
│       │   │   ├── ast_editing.py
│       │   │   ├── format_examples.py
│       │   │   └── transform.py
│       │   ├── __init__.py
│       │   └── logger.py
│       ├── __init__.py
│       └── __main__.py
├── tests
│   ├── _mock_data
│   │   ├── mock_src
│   │   │   ├── __init__.py
│   │   │   └── mod_a.py
│   │   └── tests
│   │       ├── __init__.py
│   │       ├── conftest.py
│   │       └── test_mod_a.py
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
