# Coding: UTF-8

# Copyright (C) 2025 Michał Prędki
# Licensed under the GNU General Public License v3.0.
# Full text of the license can be found in the LICENSE file in the repository.

from dataclasses import dataclass
from typing import Literal, Optional


@dataclass
class InputFilesParams:
    """Gather parameters for reading input files."""

    measurements_file_path: str = ""
    controls_file_path: str = ""


@dataclass
class AdjustmentParams:
    """Gather parameters for adjustment computation."""

    observation_weighting_method: str = "weighted"
    observation_tuning_constants: Optional[dict] = None
    perform_free_adjustment: bool = False
    free_adjustment_weighting_method: str = "weighted"
    free_adjustment_tuning_constants: Optional[dict] = None


@dataclass
class ReportParams:
    """Gather parameters for report output."""

    export_report: bool = False
    report_path: str = ""


@dataclass
class OutputParams:
    """Gather parameters for output saving."""

    output_saving_mode: Literal["Temporary layer", "To file"] = "Temporary layer"
    output_path: str = ""
