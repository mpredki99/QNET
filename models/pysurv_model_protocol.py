# Coding: UTF-8

# Copyright (C) 2025 Michał Prędki
# Licensed under the GNU General Public License v3.0.
# Full text of the license can be found in the LICENSE file in the repository.

from typing import Protocol

import pysurv as ps

from ..dto.data_transfer_objects import AdjustmentParams, InputFilesParams, ReportParams


class PySurvModel(Protocol):
    def create_project(self, input_files_params: InputFilesParams) -> ps.Project:
        """Create a PySurv Project from input file parameters with error handling."""
        ...

    def adjust(self, project: ps.Project, adjustment_params: AdjustmentParams) -> None:
        """Perform adjustment on a given pysurv project object."""
        ...

    def export_report(self, project: ps.Project, report_params: ReportParams) -> None:
        """Export adjustment report file."""
        ...
