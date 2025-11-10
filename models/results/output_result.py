# Coding: UTF-8

# Copyright (C) 2025 Michał Prędki
# Licensed under the GNU General Public License v3.0.
# Full text of the license can be found in the LICENSE file in the repository.

from .result import Result


class OutputResult(Result):
    """Result class for QGIS layer output creation operations."""

    _success_title = "Output Created"
    _warning_title = "Output Warning"
    _error_title = "Output Error"
