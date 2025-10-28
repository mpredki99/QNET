# Coding: UTF-8

# Copyright (C) 2025 Michał Prędki
# Licensed under the GNU General Public License v3.0.
# Full text of the license can be found in the LICENSE file in the repository.

from dataclasses import dataclass
from enum import Enum
from typing import Any, Optional


class ResultStatus(Enum):
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"


@dataclass
class Result:
    status: ResultStatus
    title: str
    message: str
    output: Optional[Any] = None

    def __init__(
        self,
        status: ResultStatus,
        title: str,
        message: str,
        output: Optional[Any] = None,
    ) -> None:
        self.status = status
        self.title = title
        self.message = message
        self.output = output

    def __iter__(self):
        """Enables unpacking the object: status, title, message, output = Result()."""
        yield self.status
        yield self.title
        yield self.message
        yield self.output

    @classmethod
    def success(cls, title: str, message: str, output: Optional[Any] = None):
        return cls(ResultStatus.SUCCESS, title, message, output=output)

    @classmethod
    def warning(cls, title: str, message: str, output: Optional[Any] = None):
        return cls(ResultStatus.WARNING, title, message, output=output)

    @classmethod
    def error(cls, title: str, message: str, output: Optional[Any] = None):
        return cls(ResultStatus.ERROR, title, message, output=output)
