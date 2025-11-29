# Coding: UTF-8

# Copyright (C) 2025 Michał Prędki
# Licensed under the GNU General Public License v3.0.
# Full text of the license can be found in the LICENSE file in the repository.

from typing import Optional

from qgis.core import Qgis
from qgis.utils import iface

from ..view_models.main_view_model import MainViewModel
from .base_views import BaseView
from .components.widgets import (
    QNetErrorMessageBox,
    QNetInformationMessageBox,
    QNetWarningMessageBox,
)
from .main_view_ui import MainViewUI


class MainView(MainViewUI, BaseView[MainViewModel]):
    """
    Main dialog logic for the QNET plugin.

    Integrates the top-level user interface of the QNET plugin with its corresponding
    `MainViewModel`, orchestrating all sub-views and managing user interactions. This
    class acts as the central coordinator for input handling, execution of the network
    adjustment process, and displaying the messages.

    Attributes
    ----------
    - view_model : MainViewModel
        The main view model coordinating the data flow and logic across all view sections.
    - input_file_view : InputFilesView
        Sub-view handling measurement and control input file selection.
    - weighting_methods_view : WeightingMethodsView
        Sub-view managing observation and free adjustment weighting methods configurations.
    - report_view : ReportView
        Sub-view managing report generation and export settings.
    - output_view : OutputView
        Sub-view handling QGIS layer output path selection and saving mode options.
    - ok_button : QPushButton
        Main action button used to execute the adjustment process.
    """

    def __init__(self, main_view_model: Optional[MainViewModel] = None) -> None:
        """
        Initialize the MainView.

        Parameters
        ----------
        - view_model : MainViewModel, optional
            Reference to the associated MainViewModel.
        """
        super().__init__()

        self.view_model = main_view_model or MainViewModel()

        self.input_file_view.view_model = self.view_model.input_files_view_model
        self.weighting_methods_view.view_model = (
            self.view_model.weighting_methods_view_model
        )
        self.report_view.view_model = self.view_model.report_view_model
        self.output_view.view_model = self.view_model.output_view_model

    def bind_widgets(self) -> None:
        """Bind UI widget signals to their ViewModel handlers."""
        self.ok_button.clicked.connect(self.perform_adjustment)

    def bind_view_model_signals(self) -> None:
        """Bind ViewModel signals to UI update methods."""
        self.view_model.error_occurred.connect(self.display_error_message)
        self.view_model.warning_occurred.connect(self.display_warning_message)
        self.view_model.success_occurred.connect(self.display_info_message)
        self.view_model.adjustment_in_progress.connect(
            self.display_adjustment_in_progress_message_bar
        )

    def perform_adjustment(self) -> None:
        """Execute the network adjustment calcualtions."""
        self.view_model.perform_adjustment()

    def display_error_message(self, error_type: str, error_message: str) -> None:
        """Display an error message box for the user."""
        QNetErrorMessageBox(error_type, error_message, parent=self)

    def display_warning_message(self, warning_type: str, warning_message: str) -> None:
        """Display an warning message box for the user."""
        QNetWarningMessageBox(warning_type, warning_message, parent=self)

    def display_info_message(self, info_type: str, info_message: str) -> None:
        """Display an information message box for the user."""
        QNetInformationMessageBox(info_type, info_message, parent=self)

    def display_adjustment_in_progress_message_bar(self) -> None:
        """Display an error message bar when adjustment is already in progress."""
        iface.messageBar().pushMessage(
            "Adjustment in progress",
            "An adjustment operation is already in progress. "
            "Please wait for it to complete before starting a new one.",
            level=Qgis.Critical,
            duration=3,
        )
