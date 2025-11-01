# Coding: UTF-8

# Copyright (C) 2025 Michał Prędki
# Licensed under the GNU General Public License v3.0.
# Full text of the license can be found in the LICENSE file in the repository.

from dataclasses import dataclass
from enum import Enum
from typing import Any, ClassVar, Iterator, Optional


class ResultStatus(Enum):
    """Enum class for result status."""

    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"


@dataclass
class Result:
    """
    Base class for operation results in the QNET plugin.

    Uses the Template Method pattern where subclasses define title prefixes
    via class attributes, and the base class implements the factory methods.
    """

    status: ResultStatus
    title: str
    message: str
    output: Optional[Any] = None

    # ClassVars to be overridden by subclasses to provide default titles for different result statuses
    _success_title: ClassVar[str] = ""
    _warning_title: ClassVar[str] = ""
    _error_title: ClassVar[str] = ""

    def __iter__(self) -> Iterator[Any]:
        """Enables unpacking the object: status, title, message, output = Result()."""
        yield self.status
        yield self.title
        yield self.message
        yield self.output

    @classmethod
    def _get_title(cls, status: ResultStatus) -> str:
        """Get the title for a given status."""
        titles = {
            ResultStatus.SUCCESS: cls._success_title,
            ResultStatus.WARNING: cls._warning_title,
            ResultStatus.ERROR: cls._error_title,
        }
        return titles.get(status, "")

    @classmethod
    def success(
        cls, message: str, output: Optional[Any] = None, title: Optional[str] = None
    ) -> "Result":
        """Return a SUCCESS Result with a given message and optional output and custom title."""
        result_title = (
            title if title is not None else cls._get_title(ResultStatus.SUCCESS)
        )
        if not result_title:
            result_title = "QNET Success"
        return cls(ResultStatus.SUCCESS, result_title, message, output=output)

    @classmethod
    def warning(
        cls, message: str, output: Optional[Any] = None, title: Optional[str] = None
    ) -> "Result":
        """Return a WARNING Result with a given message and optional output and custom title."""
        result_title = (
            title if title is not None else cls._get_title(ResultStatus.WARNING)
        )
        if not result_title:
            result_title = "QNET Warning"
        return cls(ResultStatus.WARNING, result_title, message, output=output)

    @classmethod
    def error(
        cls, message: str, output: Optional[Any] = None, title: Optional[str] = None
    ) -> "Result":
        """Return an ERROR Result with a given message and optional output and custom title."""
        result_title = (
            title if title is not None else cls._get_title(ResultStatus.ERROR)
        )
        if not result_title:
            result_title = "QNET Error"
        return cls(ResultStatus.ERROR, result_title, message, output=output)
