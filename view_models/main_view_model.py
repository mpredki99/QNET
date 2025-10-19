# Coding: UTF-8

# Copyright (C) 2025 Michał Prędki
# Licensed under the GNU General Public License v3.0.
# Full text of the license can be found in the LICENSE file in the repository.

import os.path
from typing import Optional

from qgis.PyQt.QtCore import QObject, pyqtSignal

from ..models import Models
from ..qnet_exceptions import QNetException
from .input_files_view_model import InputFilesViewModel
from .output_view_model import OutputViewModel
from .report_view_model import ReportViewModel
from .weighting_methods_view_model import WeightingMethodsViewModel


class MainViewModel(QObject):
    """
    Main view model for the QNET plugin.

    Coordinates and manages the interaction between all view models corresponding to UI sections,
    such as input files, weighting methods, report options, and output options. Acts as the
    central point for invoking processes like adjustment calculation and output/export tasks,
    and provides the data and logic backbone for the main dialog.
    """

    error_occured = pyqtSignal(str, str)
    warining_occured = pyqtSignal(str, str)
    info_occured = pyqtSignal(str, str)

    def __init__(
        self,
        model: Optional[Models] = None,
        input_files_view_model=InputFilesViewModel(),
        weighting_methods_view_model=WeightingMethodsViewModel(),
        report_view_model=ReportViewModel(),
        output_view_model=OutputViewModel(),
    ) -> None:
        super().__init__()

        self.pysurv_model = model.pysurv_model
        self.qgis_model = model.qgis_model

        self.input_files_view_model = input_files_view_model
        self.weighting_methods_view_model = weighting_methods_view_model
        self.report_view_model = report_view_model
        self.output_view_model = output_view_model

    def perform_adjustment(self) -> None:
        """Perform the network adjustment and export results."""
        try:
            project = self.pysurv_model.create_project(
                self.input_files_view_model.params
            )

            warning = self.pysurv_model.adjust(
                project, self.weighting_methods_view_model.params
            )
            if warning:
                self.warining_occured.emit(warning.type, warning.message)

            if self.report_view_model.params.export_report:
                if not self.report_view_model.params.report_path:
                    self.report_view_model.update_report_path(
                        os.path.join(
                            os.path.dirname(
                                self.input_files_view_model.params.controls_file_path
                            ),
                            "report.txt",
                        )
                    )
                if project.adjustment is not None:
                    self.pysurv_model.export_report(
                        project, self.report_view_model.params
                    )
                    self.info_occured.emit(
                        "Report exported",
                        f"Report file has been exported: {self.report_view_model.params.report_path}",
                    )

            output_methods = {
                "Temporary layer": self.qgis_model.create_output_layer,
                "To file": self.qgis_model.create_output_file,
            }
            output_method = output_methods.get(
                self.output_view_model.params.output_saving_mode
            )
            output_method(project, self.output_view_model.params)

        except QNetException as err:
            self.error_occured.emit(err.type, err.message)

        # self.output_view_model.export_output_file()
