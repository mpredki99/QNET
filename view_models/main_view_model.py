# Coding: UTF-8

# Copyright (C) 2025 Michał Prędki
# Licensed under the GNU General Public License v3.0.
# Full text of the license can be found in the LICENSE file in the repository.

from functools import partial
from pathlib import Path
from typing import Callable, List, Optional

from pysurv import Project
from qgis.core import QgsApplication
from qgis.PyQt.QtCore import pyqtSignal

from ..dto.data_transfer_objects import OutputParams
from ..models.main_model import MainModel
from ..models.pysurv_model import PySurvModel
from ..models.qgis_model import QGisModel
from ..models.results.result import Result, ResultStatus
from ..utils.tasks.qnet_background_task import QNetBackgroundTask
from .base_view_models import BaseViewModel
from .input_files_view_model import InputFilesViewModel
from .output_view_model import OutputViewModel
from .report_view_model import ReportViewModel
from .weighting_methods_view_model import WeightingMethodsViewModel


class MainViewModel(BaseViewModel):
    """
    Main ViewModel serving as the central orchestrator for all QNET workflows.

    This class serves as the central coordinator, managing the communication between
    the plugin's View and Model layers. It organizes and integrates all sub-ViewModels
    for tasks such as input file selection, weighting method configuration, report file
    exportation, and creating of QGIS output layer. It manages and executes the full
    network adjustment process and QGIS Vector Point layer creation by invoking proper
    models.

    Signals
    -------
    - error_occurred : pyqtSignal(str, str)
        Emitted when an error occurs during any step of the workflow.
    - warning_occurred : pyqtSignal(str, str)
        Emitted when a non-fatal issue in the workflow.
    - success_occurred : pyqtSignal(str, str)
        Emitted when a model process completes successfully.
    - adjustment_in_progress : pyqtSignal()
        Emitted if an adjustment is requested while another one is already running.

    Attributes
    ----------
    - input_files_view_model : InputFilesViewModel
        Manages state and signals related to input files selection.
    - weighting_methods_view_model : WeightingMethodsViewModel
        Handles configuration of weighting methods and tuning constants.
    - report_view_model : ReportViewModel
        Manages report export parameters.
    - output_view_model : OutputViewModel
        Manages QGIS layer output saving mode and file export options.
    - pysurv_model : PySurvModel
        Interface for performing network adjustment and report generation logic.
    - qgis_model : QGisModel
        Handles creation of QGIS output layer.
    """

    error_occurred = pyqtSignal(str, str)
    warning_occurred = pyqtSignal(str, str)
    success_occurred = pyqtSignal(str, str)
    adjustment_in_progress = pyqtSignal()

    def __init__(
        self,
        model: Optional[MainModel] = None,
        input_files_view_model: Optional[InputFilesViewModel] = None,
        weighting_methods_view_model: Optional[WeightingMethodsViewModel] = None,
        report_view_model: Optional[ReportViewModel] = None,
        output_view_model: Optional[OutputViewModel] = None,
    ) -> None:
        """
        Initialize the MainViewModel and its dependencies.

        Parameters
        ----------
        - model : MainModel, optional
            The main model instance containing references to PySurvModel and QGisModel.
            Instantiated if not provided.
        - input_files_view_model : InputFilesViewModel, optional
            ViewModel managing input file parameters. Instantiated if not provided.
        - weighting_methods_view_model : WeightingMethodsViewModel, optional
            ViewModel for weighting methods and tuning constants. Instantiated if not provided.
        report_view_model : Optional[ReportViewModel], default=None
            ViewModel for report export options. Instantiated if not provided.
        output_view_model : Optional[OutputViewModel], default=None
            ViewModel for QGIS output saving options. Instantiated if not provided.
        """
        super().__init__()

        self.pysurv_model = model.pysurv_model if model else PySurvModel()
        self.qgis_model = model.qgis_model if model else QGisModel()

        self.input_files_view_model = input_files_view_model or InputFilesViewModel()
        self.weighting_methods_view_model = (
            weighting_methods_view_model or WeightingMethodsViewModel()
        )
        self.report_view_model = report_view_model or ReportViewModel()
        self.output_view_model = output_view_model or OutputViewModel()

    def perform_adjustment(self) -> None:
        """Perform the network adjustment and export results."""
        pysurv_task = QNetBackgroundTask()
        task_manager = QgsApplication.taskManager()

        if self._adjustment_in_progress():
            self.adjustment_in_progress.emit()
            return  # Prevent multiple concurrent adjustments

        pysurv_task.add_step(
            partial(
                self.pysurv_model.create_project, self.input_files_view_model.params
            ),
            emit_signal=False,
        ).add_step(
            partial(
                self.pysurv_model.adjust,
                self.weighting_methods_view_model.params,
            ),
            emit_signal=False,
        ).add_step(
            partial(self.pysurv_model.export_report, self.report_view_model.params),
            skip=not self.report_view_model.params.export_report,
            prepare_func=self._prepare_report_path,
            emit_signal=True,
        )

        pysurv_task_results_handler = lambda: self._handle_pysurv_results(
            pysurv_task.results()
        )

        pysurv_task.taskCompleted.connect(pysurv_task_results_handler)
        pysurv_task.taskTerminated.connect(pysurv_task_results_handler)

        task_manager.addTask(pysurv_task)

    def _handle_pysurv_results(self, results: List[Result]) -> None:
        """Emit PySurv results signals and run QGIS task if no error occured."""
        if not self._emit_results_signals(results):
            return
        # Run QGIS task if no error occured
        self._run_qgis_task()

    def _run_qgis_task(self) -> bool:
        """Run the QGIS task to generate Vector Point layer."""
        qgis_task = QNetBackgroundTask()
        task_manager = QgsApplication.taskManager()

        if self._adjustment_in_progress():
            self.adjustment_in_progress.emit()
            return  # Prevent multiple concurrent adjustments

        qgis_task.add_step(
            partial(
                self._get_output_saving_mode_handler(),
                self.pysurv_model.project,
                self.output_view_model.params,
            ),
            emit_signal=False,
        )

        qgis_task_results_handler = lambda: self._emit_results_signals(
            qgis_task.results()
        )

        qgis_task.taskCompleted.connect(qgis_task_results_handler)
        qgis_task.taskTerminated.connect(qgis_task_results_handler)

        task_manager.addTask(qgis_task)

    def _prepare_report_path(self) -> None:
        """Set default report path (control points directory) if were not specified."""
        if self.report_view_model.params.report_path:
            return

        controls_file_dir = Path(
            self.input_files_view_model.params.controls_file_path
        ).parent

        self.report_view_model.update_report_path(
            str(controls_file_dir.joinpath("report.txt"))
        )

    def _get_output_saving_mode_handler(
        self,
    ) -> Optional[Callable[[Project, OutputParams], Result]]:
        """Return output handler method based on the selected output saving mode."""
        output_methods = {
            "Temporary layer": self.qgis_model.create_output_layer,
            "To file": self.qgis_model.create_output_file,
        }
        return output_methods.get(self.output_view_model.params.output_saving_mode)
    
    def _adjustment_in_progress(self) -> bool:
        """Return True if adjustment calculations is already in progress."""
        task_manager = QgsApplication.taskManager()
        return any(
            isinstance(task, QNetBackgroundTask)
            for task in task_manager.activeTasks()
        )

    def _emit_results_signals(self, results: List[Result]) -> bool:
        """Emit signals for results. Return False on error occured."""
        for result in results:
            self._emit_result_signal(result)

            if result.status == ResultStatus.ERROR:
                return False
        return True

    def _emit_result_signal(self, result: Result) -> None:
        """Emit signal corresponding to the result status."""
        signals = {
            ResultStatus.SUCCESS: self.success_occurred,
            ResultStatus.WARNING: self.warning_occurred,
            ResultStatus.ERROR: self.error_occurred,
        }
        signal = signals.get(result.status)
        signal.emit(result.title, result.message)
