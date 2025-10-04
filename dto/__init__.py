# Coding: UTF-8

# Copyright (C) 2025 Michał Prędki
# Licensed under the GNU General Public License v3.0.
# Full text of the license can be found in the LICENSE file in the repository.

"""
DTO (Data Transfer Objects) for transferring parameters 
and configuration between layers of the application.
"""

from .data_transfer_objects import (
    AdjustmentParams,
    OutputParams,
    ReaderParams,
    ReportParams,
)

__all__ = ["ReaderParams", "AdjustmentParams", "ReportParams", "OutputParams"]
