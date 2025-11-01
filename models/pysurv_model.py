# Coding: UTF-8

# Copyright (C) 2025 Michał Prędki
# Licensed under the GNU General Public License v3.0.
# Full text of the license can be found in the LICENSE file in the repository.

import warnings
from pathlib import Path
from typing import Optional

import pysurv as ps
from pysurv.exceptions import (
    EmptyDatasetError,
    InvalidDataError,
    MissingMandatoryColumnsError,
)
from pysurv.warnings import PySurvWarning

from ..dto.data_transfer_objects import AdjustmentParams, InputFilesParams, ReportParams
from .results.adjustment_result import AdjustmentResult
from .results.import_result import ImportResult
from .results.report_result import ReportResult
from .results.result import Result


class PySurvModel:
    def __init__(self) -> None:
        self._project: Optional[ps.Project] = None

    def __bool__(self) -> bool:
        return self.project is not None

    @property
    def project(self) -> Optional[ps.Project]:
        return self._project

    def create_project(self, input_files_params: InputFilesParams) -> Result:
        try:
            project = ps.Project.from_csv(
                input_files_params.measurements_file_path,
                input_files_params.controls_file_path,
            )
            self._project = project
            return ImportResult.success(
                "Files were imported successfully", output=self.project
            )

        except (
            FileNotFoundError,
            MissingMandatoryColumnsError,
            EmptyDatasetError,
        ) as err:
            return ImportResult.error(str(err))

        except InvalidDataError as err:
            dir_name = Path(input_files_params.measurements_file_path).parent
            validation_report = dir_name.joinpath("Validation_report.txt")

            with open(validation_report, "w") as file:
                file.write(str(err))

            return ImportResult.error(
                f"Invalid data occured. Please find validation report for more details: {validation_report}"
            )

        except Exception as err:
            return ImportResult.error(str(err))

    def adjust(self, adjustment_params: AdjustmentParams) -> Result:
        # Unpack the params
        obs_adj = adjustment_params.observation_weighting_method
        obs_tuning_constants = adjustment_params.observation_tuning_constants
        free_adjustment = (
            adjustment_params.free_adjustment_weighting_method
            if adjustment_params.perform_free_adjustment
            else None
        )
        free_adj_tuning_constants = (
            adjustment_params.free_adjustment_tuning_constants
            if adjustment_params.perform_free_adjustment
            else None
        )

        with warnings.catch_warnings(record=True) as warns:
            warnings.simplefilter("always", category=PySurvWarning)
            try:
                # Perform the adjustment
                self.project.adjust(
                    obs_adj=obs_adj,
                    obs_tuning_constants=obs_tuning_constants,
                    free_adjustment=free_adjustment,
                    free_adj_tuning_constants=free_adj_tuning_constants,
                )
            except Exception as err:
                return AdjustmentResult.error(str(err), output=self.project)

            if warns:
                return AdjustmentResult.warning(
                    message=str(warns[-1].message), output=self.project.adjustment
                )

            return AdjustmentResult.success(
                "Adjustment converged successfully.", output=self.project.adjustment
            )

    def export_report(self, report_params: ReportParams) -> Result:
        """Export adjustment report file."""
        try:
            self.project.adjustment.report.to_txt(report_params.report_path)
            return ReportResult.success(
                f"Report has been exported {report_params.report_path}",
                output=self.project.adjustment.report,
            )
        except Exception as err:
            return ReportResult.error(str(err))
