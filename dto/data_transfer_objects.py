# Coding: UTF-8

# Copyright (C) 2025 Michał Prędki
# Licensed under the GNU General Public License v3.0.
# Full text of the license can be found in the LICENSE file in the repository.

from dataclasses import dataclass
from typing import Optional


@dataclass
class ReaderParams:
    """Gather parameters for reading input files."""

    measurements_file_path: str
    controls_file_path: str


@dataclass
class AdjustmentParams:
    """Gather parameters for adjustment computation."""

    obs_adj: str = "weighted"
    obs_tuning_constants: Optional[dict] = None
    free_adjustment: Optional[str] = None
    free_adj_tuning_constants: Optional[dict] = None


@dataclass
class ReportParams:
    """Gather parameters for report output."""

    report_path: Optional[str] = None


@dataclass
class OutputParams:
    """Gather parameters for output saving."""

    output_saving_mode: str
    output_path: Optional[str] = None
