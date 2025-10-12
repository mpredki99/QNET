# Coding: UTF-8

# Copyright (C) 2025 Michał Prędki
# Licensed under the GNU General Public License v3.0.
# Full text of the license can be found in the LICENSE file in the repository.

from typing import Optional

from ..view_models import MainViewModel
from .main_view_ui import MainViewUI


class MainView(MainViewUI):
    """
    Main dialog logic for the QNET plugin.

    Handles user interactions, file selection, weighting method configuration,
    report and output options, and binds UI events to logic.
    """

    def __init__(self, main_view_model: Optional[MainViewModel] = None) -> None:
        super().__init__()

        self.main_view_model = main_view_model

        self.input_file_view.view_model = self.main_view_model.input_files_view_model
        self.weighting_methods_view.view_model = (
            self.main_view_model.weighting_methods_view_model
        )
        self.report_view.view_model = self.main_view_model.report_view_model
        self.output_view.view_model = self.main_view_model.output_view_model

        self.bind_widgets()

    def perform_adjustment(self) -> None:
        """Perform the adjustment."""
        self.main_view_model.perform_adjustment()

    def bind_widgets(self) -> None:
        """Bind widget signals to their respective handlers."""
        self.ok_button.clicked.connect(self.perform_adjustment)
