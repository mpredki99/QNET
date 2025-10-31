# Coding: UTF-8

# Copyright (C) 2025 Michał Prędki
# Licensed under the GNU General Public License v3.0.
# Full text of the license can be found in the LICENSE file in the repository.

from functools import partial
from pathlib import Path
from typing import Callable, Optional

from pysurv import Project
from qgis.PyQt.QtCore import pyqtSignal

from ..dto.data_transfer_objects import OutputParams
from ..models.main_model import MainModel
from ..models.results.result import Result, ResultStatus
from .base_view_model import BaseViewModel
from .input_files_view_model import InputFilesViewModel
from .output_view_model import OutputViewModel
from .report_view_model import ReportViewModel
from .weighting_methods_view_model import WeightingMethodsViewModel
from .workflow import Workflow


class MainViewModel(BaseViewModel):
    """
    Main view model for the QNET plugin.

    Coordinates and manages the interaction between all view models corresponding to UI sections,
    such as input files, weighting methods, report options, and output options. Acts as the
    central point for invoking processes like adjustment calculation and output/export tasks,
    and provides the data and logic backbone for the main dialog.
    """

    error_occured = pyqtSignal(str, str)
    warining_occured = pyqtSignal(str, str)
    success_occured = pyqtSignal(str, str)

    def __init__(
        self,
        model: Optional[MainModel] = None,
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
        if not self._run_pysurv_workflow():
            return  # Break if pysurv workflow failed
        self._run_qgis_workflow()
        
    def _run_pysurv_workflow(self) -> bool:
        return Workflow(
            partial(self.pysurv_model.create_project, self.input_files_view_model.params),
            partial(self._emit_result_signal, emit_success=False),
        ).add_step(
            Workflow(
                partial(self.pysurv_model.adjust, self.weighting_methods_view_model.params),
                partial(self._emit_result_signal, emit_success=False),
            )
        ).add_step(
            Workflow(
                partial(self.pysurv_model.export_report, self.report_view_model.params),
                partial(self._emit_result_signal, emit_success=True),
                skip=not self.report_view_model.params.export_report,
                prepare_func=self._prepare_report_path,
            )
        ).run()

    def _run_qgis_workflow(self) -> bool:
        return Workflow(
            partial(
                self._handle_output_saving_mode(),
                self.pysurv_model.project,
                self.output_view_model.params,
            ),
            partial(self._emit_result_signal, emit_success=False),
        ).run()

    def _prepare_report_path(self) -> None:
        """Set default report path into control points directory if were not specified."""
        if self.report_view_model.params.report_path:
            return

        controls_file_dir = Path(
            self.input_files_view_model.params.controls_file_path
        ).parent

        self.report_view_model.update_report_path(
            str(controls_file_dir.joinpath("report.txt"))
        )

    def _handle_output_saving_mode(self) -> Callable[[Project, OutputParams], Result]:
        """Return output handler method based on the selected output saving mode."""
        output_methods = {
            "Temporary layer": self.qgis_model.create_output_layer,
            "To file": self.qgis_model.create_output_file,
        }
        return output_methods.get(self.output_view_model.params.output_saving_mode)

    def _emit_result_signal(self, result: Result, emit_success: bool = True) -> None:
        """Emit signal corresponding to the result status."""
        if result.status == ResultStatus.SUCCESS and not emit_success:
            return

        signals = {
            ResultStatus.SUCCESS: self.success_occured,
            ResultStatus.WARNING: self.warining_occured,
            ResultStatus.ERROR: self.error_occured,
        }
        signal = signals.get(result.status)
        signal.emit(result.title, result.message)
