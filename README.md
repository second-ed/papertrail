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
│       │   │   ├── pytest_plugin.py
│       │   │   ├── record.py
│       │   │   └── recorder.py
│       │   ├── transformation
│       │   │   ├── __init__.py
│       │   │   ├── ast_editing.py
│       │   │   └── transform_docs.py
│       │   ├── __init__.py
│       │   └── logger.py
│       ├── __init__.py
│       └── __main__.py
├── tests
│   └── core
│       ├── collection
│       │   ├── __init__.py
│       │   ├── test_example.py
│       │   ├── test_record.py
│       │   └── test_recorder.py
│       └── transformation
│           ├── __init__.py
│           ├── test_ast_editing.py
│           └── test_transform_docs.py
├── .pre-commit-config.yaml
├── README.md
├── pyproject.toml
├── ruff.toml
└── uv.lock

(generated with repo-mapper-rs)
::
```
