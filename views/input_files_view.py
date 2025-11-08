# Coding: UTF-8

# Copyright (C) 2025 Michał Prędki
# Licensed under the GNU General Public License v3.0.
# Full text of the license can be found in the LICENSE file in the repository.

from typing import Optional

from ..view_models.input_files_view_model import InputFilesViewModel
from .base_views import BaseViewSection
from .components.utils import get_file_path_from_dialog, update_line_edit
from .input_files_view_ui import InputFilesViewUI


class InputFilesView(InputFilesViewUI, BaseViewSection[InputFilesViewModel]):
    """
    View class for the Input Files section in the QNET plugin.

    This class connects the Input Files UI with its corresponding `InputFilesViewModel`,
    enabling two-way data binding between user interactions and application state.
    It manages the logic for selecting and displaying the paths of the input files.
    The class binds UI widget events to ViewModel handlers and updates the interface 
    in response to ViewModel signals.

    Attributes
    ----------
    - FILE_FILTER : str
        File type filter applied to the file selection dialogs.
    - view_model : Optional[InputFilesViewModel]
        Reference to the associated ViewModel managing input file paths.
    """

    FILE_FILTER = "CSV Files (*.csv)"

    def __init__(self, view_model: Optional[InputFilesViewModel] = None) -> None:
        """
        Initialize the InputFilesView.

        Parameters
        ----------
        - view_model : InputFilesViewModel, optional
            Reference to the associated InputFilesViewModel.
        """
        super().__init__()
        self.view_model = view_model

    def bind_widgets(self) -> None:
        """Bind UI widget signals to their ViewModel handlers."""
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
        """Bind ViewModel signals to UI update methods."""
        self.view_model.measurements_file_path_changed.connect(
            self.update_measurements_line_edit
        )
        self.view_model.controls_file_path_changed.connect(
            self.update_controls_line_edit
        )

    def update_measurements_line_edit(self, measurements_file_path: str) -> None:
        """Update the measurements line edit with new file path."""
        update_line_edit(self.measurements_line_edit, measurements_file_path)

    def update_controls_line_edit(self, controls_file_path: str) -> None:
        """Update the controls line edit with new file path."""
        update_line_edit(self.controls_line_edit, controls_file_path)

    def set_measurements_file_path_from_dialog(self) -> None:
        """Open file dialog and set measurements file path."""
        path = self._get_file_path_from_dialog(self.measurements_label.text()[:-1])
        if path:
            self.view_model.update_measurements_file_path(path)

    def set_controls_file_path_from_dialog(self) -> None:
        """Open file dialog and set controls file path."""
        path = self._get_file_path_from_dialog(self.controls_label.text()[:-1])
        if path:
            self.view_model.update_controls_file_path(path)

    def _get_file_path_from_dialog(self, window_title: str) -> str:
        """Open file dialog and return the selected path."""
        return get_file_path_from_dialog(
            self, window_title, "", self.FILE_FILTER, "open"
        )
