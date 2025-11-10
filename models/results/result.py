# Coding: UTF-8

# Copyright (C) 2025 Michał Prędki
# Licensed under the GNU General Public License v3.0.
# Full text of the license can be found in the LICENSE file in the repository.

from dataclasses import dataclass
from enum import Enum
from typing import Any, ClassVar, Iterator, Optional


class ResultStatus(Enum):
    """
    Enumeration defining possible statuses for a `Result` object.

    Attributes
    ----------
    - SUCCESS : str
        Indicates the operation completed successfully.
    - WARNING : str
        Indicates the operation completed with warnings or non-critical issues.
    - ERROR : str
        Indicates the operation failed due to an error.
    """

    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"


@dataclass
class Result:
    """
    Base class for returning operation results used across QNET models.

    The `Result` class encapsulates the outcome of a model operation, including its
    status (`ResultStatus`), human-readable title, descriptive message, and optional
    output data. It is designed for subclassing, with specialized subclasses providing
    default titles appropriate to specific operation types.

    Attributes
    ----------
    - status : ResultStatus
        The status of the operation (SUCCESS, WARNING, or ERROR).
    - title : str
        Short descriptive title summarizing the result context.
    - message : str
        Detailed message describing the operation outcome.
    - output : Any, optional
        Optional return value containing data produced by the operation.

    Class Variables
    ---------------
    - _success_title : str
        Default title for success results (to be overridden by subclasses).
    - _warning_title : str
        Default title for warning results (to be overridden by subclasses).
    - _error_title : str
        Default title for error results (to be overridden by subclasses).

    Methods
    -------
    success(message: str, output: Any = None, title: str | None = None) -> Result
        Create a Result object representing a successful operation.
    warning(message: str, output: Any = None, title: str | None = None) -> Result
        Create a Result object representing a warning state.
    error(message: str, output: Any = None, title: str | None = None) -> Result
        Create a Result object representing an error state.
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
        """Return the appropriate title based on the given status."""
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
