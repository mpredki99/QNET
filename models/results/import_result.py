# Coding: UTF-8

# Copyright (C) 2025 Michał Prędki
# Licensed under the GNU General Public License v3.0.
# Full text of the license can be found in the LICENSE file in the repository.

from .result import Result


class ImportResult(Result):
    """Result class for import file operations."""

    _success_title = "Import Files Complete"
    _warning_title = "Import Files Warning"
    _error_title = "Import Files Error"
