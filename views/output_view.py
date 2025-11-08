# Coding: UTF-8

# Copyright (C) 2025 Michał Prędki
# Licensed under the GNU General Public License v3.0.
# Full text of the license can be found in the LICENSE file in the repository.

from functools import partial
from typing import Optional

from ..view_models.output_view_model import OutputViewModel
from .base_views import BaseViewSection
from .components.utils import get_file_path_from_dialog, update_line_edit
from .output_view_ui import OutputViewUI


class OutputView(OutputViewUI, BaseViewSection[OutputViewModel]):
    """
    View class for the QGIS output section in the QNET plugin.

    This class connects the Output View UI with its corresponding `OutputViewModel`,
    enabling two-way data binding between user interactions and application state.
    It manages the logic for saving the output file allowing users to choose between
    saving results to a file or a temporary QGIS layer. It connects the UI widget
    events to ViewModel handlers with the corresponding and updates the interface
    in response to ViewModel signals.

    Attributes
    ----------
    - FILE_FILTER : str
        File type filter used in the output file dialog.
    """

    FILE_FILTER = "Shapefile (*.shp)"

    def __init__(self, view_model: Optional[OutputViewModel] = None) -> None:
        """
        Initialize the OutputView.

        Parameters
        ----------
        - view_model : OutputViewModel, optional
            Reference to the associated OutputViewModel.
        """
        super().__init__()
        self.view_model = view_model

    def bind_widgets(self) -> None:
        """Bind UI widget signals to their ViewModel handlers."""
        for action in self.output_saving_mode_menu.actions():
            action.triggered.connect(
                partial(self.view_model.update_output_saving_mode, action.text())
            )

        self.output_line_edit.textChanged.connect(self.view_model.update_output_path)

    def bind_view_model_signals(self) -> None:
        """Bind ViewModel signals to UI update methods."""
        self.view_model.output_saving_mode_changed.connect(
            self.handle_output_saving_mode
        )
        self.view_model.output_path_changed.connect(self.update_output_line_edit)

    def handle_output_saving_mode(self, output_saving_mode: str) -> None:
        """Determines and run the appropriate method when the saving mode changes."""
        output_handlers = {
            "Temporary layer": partial(self.update_output_line_edit, ""),
            "To file": self.update_output_line_edit_from_dialog,
        }
        output_handler = output_handlers.get(output_saving_mode)
        if output_handler:
            output_handler()

    def update_output_line_edit(self, output_path: str) -> None:
        """Update the output line edit with a new output file path."""
        update_line_edit(self.output_line_edit, output_path)

    def update_output_line_edit_from_dialog(self) -> None:
        """Open file dialog and return the selected path."""
        path = get_file_path_from_dialog(
            self, self.output_label.text()[:-1], "", self.FILE_FILTER, "save"
        )

        if path:
            update_line_edit(self.output_line_edit, path)
