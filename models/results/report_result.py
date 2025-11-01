# Coding: UTF-8

# Copyright (C) 2025 Michał Prędki
# Licensed under the GNU General Public License v3.0.
# Full text of the license can be found in the LICENSE file in the repository.

from typing import Any, Optional

from .result import Result


class ReportResult(Result):
    @classmethod
    def success(cls, message: str, output: Optional[Any] = None) -> "ReportResult":
        return super().success("Report Exported", message, output=output)

    @classmethod
    def warning(cls, message: str, output: Optional[Any] = None) -> "ReportResult":
        return super().warning("Report Warning", message, output=output)

    @classmethod
    def error(cls, message: str, output: Optional[Any] = None) -> "ReportResult":
        return super().error("Report Error", message, output=output)
