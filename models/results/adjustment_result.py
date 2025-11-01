# Coding: UTF-8

# Copyright (C) 2025 Michał Prędki
# Licensed under the GNU General Public License v3.0.
# Full text of the license can be found in the LICENSE file in the repository.

from .result import Result


class AdjustmentResult(Result):
    """Result class for adjustment operations."""

    _success_title = "Adjustment Complete"
    _warning_title = "Adjustment Warning"
    _error_title = "Adjustment Error"
