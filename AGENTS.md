# AGENTS.md - Guidelines for TexBib Development

## Project Overview
TexBib is a Python CLI tool for managing BibTeX bibliographies. It provides commands
to add, remove, search, and organize bibliographic references.

## Build/Lint/Test Commands

### Running All Tests
```bash
# Using tox (runs pytest with multiple Python versions)
tox

# Or directly with pytest
pytest
```

### Running a Single Test
```bash
# Single test file
pytest tests/test_command_init.py

# Single test function
pytest tests/test_command_init.py::test_creation

# Single test with verbose output
pytest tests/test_command_init.py::test_creation -v
```

### Installation (Development)
```bash
# Install in editable mode with test dependencies
pip install -e ".[test]"
```

### Running the CLI Locally
```bash
# After installation
bib --help

# Or run directly
python -m texbib --help
```

## Code Style Guidelines

### General
- Use **4 spaces** for indentation (no tabs)
- Maximum line length: **100 characters** (soft limit)
- All source files should have `# -*- coding: utf-8 -*-` header
- Use docstrings for all public modules, classes, and functions

### Imports
- Standard library imports first, then third-party, then local
- Use relative imports for internal texbib modules (`from .module import ...`)
- Use absolute imports for external packages
- Group imports by type with blank lines between groups
```python
# Standard library
import os
import sys
import re
from pathlib import Path
from typing import List, Optional, Union

# Third-party
import bibtexparser

# Local (relative)
from .bibliography import Bibliography
from .errors import BibError, ExitCode
```

### Type Hints
- Use `typing` module for type annotations (List, Optional, Union, etc.)
- Use `pathlib.Path` for file paths, not strings
- Annotate function parameters and return types
```python
def foo(bar: str, baz: Optional[int] = None) -> List[str]:
    ...
```

### Naming Conventions
- **Classes**: PascalCase (e.g., `BibItem`, `RuntimeInstance`)
- **Functions/variables**: snake_case (e.g., `format_term`, `active_path`)
- **Constants**: SCREAMING_SNAKE_CASE (e.g., `EXIT_SUCCESS`)
- **Enums**: PascalCase for enum and members (e.g., `ExitCode.SUCCESS`)
- **Private members**: prefix with underscore (e.g., `_internal_method`)

### Docstrings
- Use Google-style docstrings
```python
class MyClass:
    """Short description of the class.

    Longer description if needed, explaining the purpose
    and usage of the class.

    Attributes:
        attr1: Description of attr1.
        attr2: Description of attr2.
    """

    def my_method(self, arg1: str, arg2: int) -> bool:
        """Short description of the method.

        Args:
            arg1: Description of arg1.
            arg2: Description of arg2.

        Returns:
            Description of return value.
        """
        ...
```

### Error Handling
- Use custom exception hierarchy based on `BibError` in `texbib/errors.py`
- Each exception should have an associated `exit_code` from `ExitCode` enum
- Return `ExitCode` values from command functions, don't raise for expected cases
```python
from texbib.errors import BibError, FileNotFound, IdNotFound, ExitCode

class MyError(BibError):
    exit_code = ExitCode.MY_ERROR_CODE

    def __init__(self, message: str):
        super().__init__(f"My error: {message}")
```

### File Structure
```
texbib/
    __init__.py          # Package init, exports public API
    __main__.py          # Entry point for python -m texbib
    cli.py               # CLI argument parsing and main()
    commands.py          # All CLI commands (decorated with @commands.register)
    bibliography.py      # BibItem and Bibliography classes
    errors.py            # Custom exceptions and ExitCode enum
    runtime.py           # RuntimeInstance for managing environment
    parser.py            # BibTeX parsing utilities
    settings.py          # Configuration handling
    utils.py              # General utility functions
    colors.py             # Terminal color utilities
    term_utils.py        # Terminal formatting utilities
    schemes.py           # URI scheme handling
    sources/
        __init__.py      # Source handlers (DOI, arXiv, ISBN, etc.)
        doi.py
        arxiv.py
        isbn.py
        file.py
```

### Testing Conventions
- Tests live in `tests/` directory
- One test file per command/module: `test_command_<name>.py`
- Use pytest fixtures defined in `tests/conftest.py`
- Use `capsys` for capturing stdout/stderr
- Use `monkeypatch` for mocking
```python
def test_my_command(commands, capsys, monkeypatch):
    monkeypatch.setattr(commands.run, 'input', lambda: 'y')
    result = commands['my_command']('arg')
    assert result == ExitCode.SUCCESS
```

### CLI Commands Pattern
Commands are registered using the `@commands.register` decorator:
```python
@commands.register
def my_command(arg1: str, arg2: Optional[str] = None) -> ExitCode:
    """Description shown in --help"""
    # Use commands.run for RuntimeInstance access
    # Return ExitCode value
    return ExitCode.SUCCESS
```

### Context Managers
Use context managers for resource management:
```python
with commands.run.open('r') as bib:
    for item in bib:
        ...
```

### Path Handling
- Always use `pathlib.Path` for file/directory paths
- Use `.exists()`, `.mkdir()`, `.unlink()` methods
- Prefer relative operations over string concatenation
