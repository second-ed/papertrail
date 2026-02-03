"""repo-map-desc: Updates the the docstrings for all the funcs in the files in the example cache.

This is the main entry point for the transformation module.
"""

from io_adapters import IoAdapter

from papertrail.adapters.io_funcs import FileType
from papertrail.core.transformation.ast_editing import update_function_docstrings
from papertrail.core.transformation.format_examples import (
    collect_example_strs,
    reduce_examples_to_example_str,
)


def update_modified_docstrings(adapter: IoAdapter, examples_cache_path: str) -> None:
    examples = adapter.read(examples_cache_path, FileType.JSON)
    reduced_examples = reduce_examples_to_example_str(collect_example_strs(examples))

    for path, module_examples in reduced_examples.items():
        code = adapter.read(path, FileType.STR)
        new_code = update_function_docstrings(code, module_examples)
        if new_code != code:
            adapter.write(new_code, path, FileType.STR)
