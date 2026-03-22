# -*- coding: utf-8 -*-
"""
Exception classes for texbib error handling.
"""


class BibError(Exception):
    """Base exception for all bib errors."""
    exit_code = 1

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class FileNotFound(BibError):
    """Raised when a file or directory is not found."""

    def __init__(self, path):
        super().__init__(f"File not found: {path}")
        self.path = path


class IdNotFound(BibError):
    """Raised when a bibliography entry ID is not found."""

    def __init__(self, identifier: str):
        super().__init__(f"Reference '{identifier}' not found")
        self.identifier = identifier


class InvalidName(BibError):
    """Raised when a bibliography name is invalid."""

    def __init__(self, name: str, reason: str | None = None):
        msg = f"Invalid bibliography name: {name}"
        if reason:
            msg += f" ({reason})"
        super().__init__(msg)
        self.name = name
        self.reason = reason


class BibExists(BibError):
    """Raised when a bibliography already exists."""

    def __init__(self, name: str):
        super().__init__(f"Bibliography '{name}' already exists")
        self.name = name
