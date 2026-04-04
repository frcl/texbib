# AGENTS.md - Guidelines for TexBib Development

## Project Overview
TexBib is a Python CLI tool for managing BibTeX bibliographies. It provides commands
to add, remove, search, and organize bibliographic references.

## Build/Lint/Test Commands

### Running All Tests
```bash
tox                     # Using tox (runs pytest with multiple Python versions)
~/.local/share/pipx/venvs/texbib/bin/python -m pytest  # Direct with pipx venv
pytest                  # If installed in editable mode
```

### Running a Single Test
```bash
~/.local/share/pipx/venvs/texbib/bin/python -m pytest tests/test_command_init.py
~/.local/share/pipx/venvs/texbib/bin/python -m pytest tests/test_command_init.py::test_creation -v
```

### Installation (Development)
```bash
pipx install -e . --pip-args=".[test]"
```

### Running the CLI Locally
```bash
bib --help
~/.local/share/pipx/venvs/texbib/bin/python -m texbib --help
```

## Code Style Guidelines

### General
- Use **4 spaces** for indentation (no tabs)
- Maximum line length: **100 characters** (soft limit)
- Use docstrings for all public modules, classes, and functions

### Imports
Standard library → third-party → local (relative). Use blank lines between groups.
```python
import os
import sys
import re
from pathlib import Path
from typing import List, Optional, Union

import bibtexparser

from .bibliography import Bibliography
from .errors import BibError, ExitCode
```

### Type Hints
Use `typing` module and `pathlib.Path` for file paths. Annotate all parameters and returns.

### Naming Conventions
- **Classes**: PascalCase (e.g., `BibItem`, `RuntimeInstance`)
- **Functions/variables**: snake_case (e.g., `format_term`, `active_path`)
- **Constants**: SCREAMING_SNAKE_CASE (e.g., `EXIT_SUCCESS`)
- **Enums**: PascalCase for enum and members (e.g., `ExitCode.SUCCESS`)
- **Private members**: prefix with underscore (e.g., `_internal_method`)

### Docstrings
Use Google-style docstrings.

### Error Handling
Use custom exception hierarchy based on `BibError` in `texbib/errors.py`. Each exception should have an associated `exit_code` from `ExitCode` enum. Return `ExitCode` values from command functions, don't raise for expected cases.

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
        doi.py, arxiv.py, isbn.py, file.py
```

### Testing Conventions
- Tests in `tests/` directory, one file per command/module (`test_command_<name>.py`)
- Use pytest fixtures from `tests/conftest.py`
- Use `capsys` for stdout/stderr, `monkeypatch` for mocking

### CLI Commands Pattern
Use `@commands.register` decorator:
```python
@commands.register
def my_command(arg1: str, arg2: Optional[str] = None) -> ExitCode:
    """Description shown in --help"""
    return ExitCode.SUCCESS
```
Use `commands.run` for RuntimeInstance access.

### Context Managers
Use context managers for resource management:
```python
with commands.run.open('r') as bib:
    for item in bib:
        ...
```

### Path Handling
Always use `pathlib.Path` for file/directory paths. Use `.exists()`, `.mkdir()`, `.unlink()` methods.