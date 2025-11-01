# Coding: UTF-8

# Copyright (C) 2025 Michał Prędki
# Licensed under the GNU General Public License v3.0.
# Full text of the license can be found in the LICENSE file in the repository.

from typing import Any, Optional

from .result import Result


class ImportResult(Result):
    @classmethod
    def success(cls, message: str, output: Optional[Any] = None) -> "ImportResult":
        return super().success("Import Files Complete", message, output=output)

    @classmethod
    def warning(cls, message: str, output: Optional[Any] = None) -> "ImportResult":
        return super().warning("Import Files Warning", message, output=output)

    @classmethod
    def error(cls, message: str, output: Optional[Any] = None) -> "ImportResult":
        return super().error("Import Files Error", message, output=output)
