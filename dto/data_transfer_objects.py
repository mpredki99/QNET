"""
========================================================================================
Data Transfer Objects (DTO)
========================================================================================

This module defines structured data containers used to transfer parameters between the 
ViewModel and Model layers of the QNET plugin.

Each dataclass encapsulates a set of related parameters used in specific stages of the
plugin's workflow — such as importing input files, performing network adjustment,
exporting reports, or saving output data. These classes also enables to set default
values of the parameters that mirror the initial state of the user interface.

Structure
---------
- `InputFilesParams`: Stores file paths for measurements and control points input.
- `AdjustmentParams`: Stores parameters for least squares adjustment computation.
- `ReportParams`: Stores report generation options and file path.
- `OutputParams`: Stores parameters for QGIS layer output saving mode and path.

========================================================================================
"""

from dataclasses import dataclass
from typing import Literal, Optional


@dataclass
class InputFilesParams:
    """
    Parameters for reading input files.

    Attributes
    ----------
    - measurements_file_path : str
        Absolute path to the measurements file containing raw observation data.
    - controls_file_path : str
        Absolute path to the control points file containing approximate coordinates.
    """

    measurements_file_path: str = ""
    controls_file_path: str = ""


@dataclass
class AdjustmentParams:
    """
    Parameters controlling the network adjustment computation.

    Attributes
    ----------
    - observation_weighting_method : str
        PySurv name of the weighting method used for observation adjustment.
    - observation_tuning_constants : Optional[dict]
        Optional dictionary of tuning constants for the observation weighting function.
    - perform_free_adjustment : bool
        Flag indicating whether a free network adjustment should be performed.
    - free_adjustment_weighting_method : str
        PySurv name of the weighting method used for free adjustment points adjustment.
    - free_adjustment_tuning_constants : Optional[dict]
        Optional dictionary of tuning constants for free adjustment weighting function.
    """

    observation_weighting_method: str = "weighted"
    observation_tuning_constants: Optional[dict] = None
    perform_free_adjustment: bool = False
    free_adjustment_weighting_method: str = "weighted"
    free_adjustment_tuning_constants: Optional[dict] = None


@dataclass
class ReportParams:
    """
    Parameters for report generation and export.

    Attributes
    ----------
    - export_report : bool
        Flag indicating whether a report should be generated and saved.
    - report_path : str
        Path to the output report file.
    """

    export_report: bool = False
    report_path: str = ""


@dataclass
class OutputParams:
    """
    Parameters for saving output data.

    Attributes
    ----------
    - output_saving_mode : Literal["Temporary layer", "To file"]
        Output saving mode: either as a temporary QGIS layer or a file written to disk.
    - output_path : str
        Path to the output file or name of the temporary layer, depending on the mode.
    """

    output_saving_mode: Literal["Temporary layer", "To file"] = "Temporary layer"
    output_path: str = ""
