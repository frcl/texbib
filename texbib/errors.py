# -*- coding: utf-8 -*-
"""
Exception classes for texbib error handling.
"""
from enum import IntEnum
from typing import Optional


class ExitCode(IntEnum):
    """Exit codes for texbib CLI commands.

    Follows Unix conventions where 0 is success and non-zero values
    indicate various error conditions.
    """
    SUCCESS = 0
    GENERAL_ERROR = 1
    USAGE_ERROR = 2
    PERMISSION_ERROR = 3
    FILE_NOT_FOUND = 4
    ID_NOT_FOUND = 5
    EXISTS = 6
    INVALID_INPUT = 7
    UNKOWN_RESOURCE = 8


class BibError(Exception):
    """Base exception for all bib errors."""
    exit_code = ExitCode.GENERAL_ERROR

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class FileNotFound(BibError):
    """Raised when a file or directory is not found."""
    exit_code = ExitCode.FILE_NOT_FOUND

    def __init__(self, path):
        super().__init__(f"File not found: {path}")
        self.path = path


class IdNotFound(BibError):
    """Raised when a bibliography entry ID is not found."""
    exit_code = ExitCode.ID_NOT_FOUND

    def __init__(self, identifier: str):
        super().__init__(f"Reference '{identifier}' not found")
        self.identifier = identifier


class InvalidName(BibError):
    """Raised when a bibliography name is invalid."""
    exit_code = ExitCode.INVALID_INPUT

    def __init__(self, name: str, reason: Optional[str] = None):
        msg = f"Invalid bibliography name: {name}"
        if reason:
            msg += f" ({reason})"
        super().__init__(msg)
        self.name = name
        self.reason = reason


class BibExists(BibError):
    """Raised when a bibliography already exists."""
    exit_code = ExitCode.EXISTS

    def __init__(self, name: str):
        super().__init__(f"Bibliography '{name}' already exists")
        self.name = name


class UnkownResource(BibError):
    """Raised when a link or file has an unknown format."""
    exit_code = ExitCode.UNKOWN_RESOURCE

    def __init__(self, resource: str):
        super().__init__(f"Invalid or unsupported resource '{resource}'")
        self.resource = resource
