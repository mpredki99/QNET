# Coding: UTF-8

# Copyright (C) 2025 Michał Prędki
# Licensed under the GNU General Public License v3.0.
# Full text of the license can be found in the LICENSE file in the repository.

from typing import Optional

from ..view_models.main_view_model import MainViewModel
from .base_views import BaseView
from .components.widgets import (
    QNetErrorMessageBox,
    QNetInformationMessageBox,
    QNetWarinigMessageBox,
)
from .main_view_ui import MainViewUI


class MainView(MainViewUI, BaseView):
    """
    Main dialog logic for the QNET plugin.

    Handles user interactions, file selection, weighting method configuration,
    report and output options, and binds UI events to logic.
    """

    def __init__(self, main_view_model: Optional[MainViewModel] = None) -> None:
        super().__init__()

        self.view_model = main_view_model

        if not self.view_model:
            return

        self.input_file_view.view_model = self.view_model.input_files_view_model
        self.weighting_methods_view.view_model = (
            self.view_model.weighting_methods_view_model
        )
        self.report_view.view_model = self.view_model.report_view_model
        self.output_view.view_model = self.view_model.output_view_model

    def bind_widgets(self) -> None:
        """Bind widget signals to their respective handlers."""
        self.ok_button.clicked.connect(self.perform_adjustment)

    def bind_view_model_signals(self) -> None:
        """Bind view model signals to UI update methods."""
        self.view_model.error_occured.connect(self.show_error_message)
        self.view_model.warining_occured.connect(self.show_warning_message)
        self.view_model.success_occured.connect(self.show_info_message)

    def perform_adjustment(self) -> None:
        """Perform the adjustment."""
        self.view_model.perform_adjustment()

    def show_error_message(self, error_type: str, error_message: str) -> None:
        """Show an error message box for the user."""
        QNetErrorMessageBox(error_type, error_message, parent=self)

    def show_warning_message(self, warning_type: str, warning_message: str) -> None:
        """Show an warning message box for the user."""
        QNetWarinigMessageBox(warning_type, warning_message, parent=self)

    def show_info_message(self, info_type: str, info_message: str) -> None:
        """Show an warning message box for the user."""
        QNetInformationMessageBox(info_type, info_message, parent=self)
