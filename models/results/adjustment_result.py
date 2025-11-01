# Coding: UTF-8

# Copyright (C) 2025 Michał Prędki
# Licensed under the GNU General Public License v3.0.
# Full text of the license can be found in the LICENSE file in the repository.

from typing import Any, Optional

from .result import Result


class AdjustmentResult(Result):
    @classmethod
    def success(cls, message: str, output: Optional[Any] = None) -> "AdjustmentResult":
        return super().success("Adjustment Complete", message, output=output)

    @classmethod
    def warning(cls, message: str, output: Optional[Any] = None) -> "AdjustmentResult":
        return super().warning("Adjustment Warning", message, output=output)

    @classmethod
    def error(cls, message: str, output: Optional[Any] = None) -> "AdjustmentResult":
        return super().error("Adjustment Error", message, output=output)
