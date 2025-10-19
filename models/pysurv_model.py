# Coding: UTF-8

# Copyright (C) 2025 Michał Prędki
# Licensed under the GNU General Public License v3.0.
# Full text of the license can be found in the LICENSE file in the repository.

import os.path
import warnings
from typing import Optional

import pysurv as ps
from pysurv.exceptions import *
from pysurv.warnings import PySurvWarning

from ..dto.data_transfer_objects import AdjustmentParams, InputFilesParams, ReportParams
from ..qnet_exceptions import AdjustmentError, InputFilesError, ReportError
from ..qnet_warnings import AdjustmentWarning, QNetWarning


def create_project(input_files_params: InputFilesParams) -> ps.Project:
    """Create a PySurv Project from input file parameters with error handling."""
    try:
        return ps.Project.from_csv(
            input_files_params.measurements_file_path,
            input_files_params.controls_file_path,
        )
    except (FileNotFoundError, MissingMandatoryColumnsError, EmptyDatasetError) as err:
        (message,) = err.args
        raise InputFilesError(message=message)

    except InvalidDataError as err:
        dir_name = os.path.dirname(input_files_params.measurements_file_path)
        validation_report = os.path.join(dir_name, "Validation_report.txt")

        (message,) = err.args
        with open(validation_report, "w") as file:
            file.write(message)

        raise InputFilesError(
            message=f"Invalid data occured. Please find validation report for more details: {validation_report}"
        )

    except:
        raise InputFilesError


def adjust(
    project: ps.Project, adjustment_params: AdjustmentParams
) -> Optional[QNetWarning]:
    """Perform adjustment on a given pysurv project object."""
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
            project.adjust(
                obs_adj=obs_adj,
                obs_tuning_constants=obs_tuning_constants,
                free_adjustment=free_adjustment,
                free_adj_tuning_constants=free_adj_tuning_constants,
            )
        except:
            raise AdjustmentError
        # Process captured warnings
        if warns:
            return AdjustmentWarning(message=str(warns[0].message))


def export_report(project: ps.Project, report_params: ReportParams) -> None:
    """Export adjustment report file."""
    try:
        project.adjustment.report.to_txt(report_params.report_path)
    except:
        raise ReportError
