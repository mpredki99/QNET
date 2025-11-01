# Coding: UTF-8

# Copyright (C) 2025 Michał Prędki
# Licensed under the GNU General Public License v3.0.
# Full text of the license can be found in the LICENSE file in the repository.

from .result import Result


class ReportResult(Result):
    """Result class for report export operations."""

    _success_title = "Report Exported"
    _warning_title = "Report Warning"
    _error_title = "Report Error"
