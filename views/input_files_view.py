# Coding: UTF-8

# Copyright (C) 2025 Michał Prędki
# Licensed under the GNU General Public License v3.0.
# Full text of the license can be found in the LICENSE file in the repository.

from typing import Optional

from ..view_models.input_files_view_model import InputFilesViewModel
from .base_view import BaseView
from .components.utils import get_file_path_from_dialog_window, update_line_edit
from .input_files_view_ui import InputFilesViewUI


class InputFilesView(InputFilesViewUI, BaseView[InputFilesViewModel]):
    """
    View class for the input files section in the QNET plugin.

    This class binds the UI widgets for selecting measurements and controls input files,
    manages their file paths, and connects user interactions to the corresponding view model
    handlers. It also updates the UI in response to changes in the view model, such as
    updating the file path fields when the underlying data changes.
    """

    file_filter = "CSV Files (*.csv)"

    def __init__(self, view_model: Optional[InputFilesViewModel] = None) -> None:
        super().__init__()
        self.view_model = view_model

    def bind_widgets(self) -> None:
        """Bind UI widgets to their handlers."""
        self.measurements_button.clicked.connect(
            self.set_measurements_file_path_from_dialog
        )
        self.measurements_line_edit.textChanged.connect(
            self.view_model.update_measurements_file_path
        )

        self.controls_button.clicked.connect(self.set_controls_file_path_from_dialog)
        self.controls_line_edit.textChanged.connect(
            self.view_model.update_controls_file_path
        )

    def bind_view_model_signals(self) -> None:
        """Bind view model signals to UI update methods."""
        self.view_model.measurements_file_path_changed.connect(
            self.update_measurements_line_edit
        )
        self.view_model.controls_file_path_changed.connect(
            self.update_controls_line_edit
        )

    def update_measurements_line_edit(self, new_measurements_file_path: str) -> None:
        """Update the measurements line edit with new file path."""
        update_line_edit(self.measurements_line_edit, new_measurements_file_path)

    def update_controls_line_edit(self, new_controls_file_path: str) -> None:
        """Update the controls line edit with new file path."""
        update_line_edit(self.controls_line_edit, new_controls_file_path)

    def set_measurements_file_path_from_dialog(self) -> None:
        """Set the measurements file path from file dialog."""
        path = self._get_file_path_from_dialog(self.measurements_label.text()[:-1])
        if path:
            self.view_model.update_measurements_file_path(path)

    def set_controls_file_path_from_dialog(self) -> None:
        """Set the controls file path from file dialog."""
        path = self._get_file_path_from_dialog(self.controls_label.text()[:-1])
        if path:
            self.view_model.update_controls_file_path(path)

    def _get_file_path_from_dialog(self, window_title: str) -> str:
        """Open file dialog and return the selected file path."""
        return get_file_path_from_dialog_window(
            self, window_title, "", self.file_filter, "open"
        )
