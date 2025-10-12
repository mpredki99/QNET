# Coding: UTF-8

# Copyright (C) 2025 Michał Prędki
# Licensed under the GNU General Public License v3.0.
# Full text of the license can be found in the LICENSE file in the repository.

from functools import partial
from typing import Optional

from ..view_models.output_view_model import OutputViewModel
from .base_view import BaseView
from .components.utils import get_file_path_from_dialog_window, update_line_edit
from .output_view_ui import OutputViewUI


class OutputView(OutputViewUI, BaseView):
    """
    Output section logic and UI for the QNET plugin.

    Handles interactions for selecting and saving output files, including output path selection and
    saving mode management. Binds UI widgets to the associated view model and synchronizes states
    and parameters for output saving.
    """

    file_filter = "Shapefile (*.shp)"

    def __init__(self, view_model: Optional[OutputViewModel] = None) -> None:
        super().__init__()
        self.view_model = view_model

    @property
    def view_model(self) -> Optional[OutputViewModel]:
        """Get the current view model."""
        return self._view_model

    @view_model.setter
    def view_model(self, view_model: Optional[OutputViewModel]) -> None:
        """Set the view model and bind widgets and signals if its not None."""
        self._view_model = view_model
        if not self._view_model:
            return
        self.bind_widgets()
        self.bind_view_model_signals()
        self._view_model.reset_state()

    def bind_widgets(self) -> None:
        """Bind UI widgets to their handlers."""
        for action in self.output_saving_mode_menu.actions():
            action.triggered.connect(
                partial(self.view_model.update_output_saving_mode, action.text())
            )

        self.output_line_edit.textChanged.connect(self.view_model.update_output_path)

    def bind_view_model_signals(self) -> None:
        """Bind view model signals to UI update methods."""
        self.view_model.output_saving_mode_changed.connect(
            self.handle_output_saving_mode
        )
        self.view_model.output_path_changed.connect(self.update_output_line_edit)

    def handle_output_saving_mode(self, output_saving_mode: str) -> None:
        """Handle change in output saving mode."""
        output_handlers = {
            "Temporary layer": partial(self.update_output_line_edit, ""),
            "To file": self.set_output_path_from_dialog,
        }
        output_handler = output_handlers.get(output_saving_mode)
        if output_handler:
            output_handler()

    def update_output_line_edit(self, output_path: str) -> None:
        """Update the output line edit widget."""
        update_line_edit(self.output_line_edit, output_path)

    def set_output_path_from_dialog(self) -> None:
        """Open file dialog and set the output path."""
        path = get_file_path_from_dialog_window(
            self, self.output_label.text()[:-1], "", self.file_filter, "save"
        )

        if path:
            update_line_edit(self.output_line_edit, path)
