# Coding: UTF-8

# Copyright (C) 2025 Michał Prędki
# Licensed under the GNU General Public License v3.0.
# Full text of the license can be found in the LICENSE file in the repository.

from functools import partial

from qgis.PyQt.QtCore import pyqtSignal

from ..dto.data_transfer_objects import OutputParams
from .base_view_models import BaseViewModelSection


class OutputViewModel(BaseViewModelSection):
    """
    View model for the output section in the QNET plugin.

    Manages state and logic for output file parameters, including output path and saving mode.
    Provides an interface between the UI and underlying command logic for exporting output files,
    encapsulating signal emission to reflect state changes to the view. Supports updating
    output saving mode (temporary layer or file), emitting changes to connected views, and
    executing the export output file command with current parameters.
    """

    output_saving_mode_changed = pyqtSignal(str)
    output_path_changed = pyqtSignal(str)

    def __init__(self, model=None) -> None:
        super().__init__()
        self.model = model

        self.params = OutputParams()

    def reset_state(self) -> None:
        """Reset the input files parameters and emit signals."""
        self.params = OutputParams()
        self._emit_output_saving_mode_changed()
        self._emit_output_path_changed()

    def update_output_saving_mode(self, output_saving_mode: str) -> None:
        """Update the output saving mode and emit the change signal."""
        output_handlers = {
            "Temporary layer": partial(
                self._set_temporary_layer_saving_output_mode, output_saving_mode
            ),
            "To file": partial(
                self._set_to_file_saving_output_mode, output_saving_mode
            ),
        }
        output_handler = output_handlers.get(output_saving_mode)
        if output_handler:
            output_handler()

    def update_output_path(self, output_path: str) -> None:
        """Update the output path and emit the change signal."""
        self.params.output_path = output_path
        self._emit_output_path_changed()

    def _set_temporary_layer_saving_output_mode(self, output_saving_mode: str) -> None:
        """Handle output mode when 'Temporary layer' is selected."""
        if self.params.output_saving_mode == "Temporary layer":
            return
        self.params.output_saving_mode = output_saving_mode
        self._emit_output_saving_mode_changed()

    def _set_to_file_saving_output_mode(self, output_saving_mode: str) -> None:
        """Handle output mode when 'To file' is selected."""
        self.params.output_saving_mode = output_saving_mode
        self._emit_output_saving_mode_changed()

    def _emit_output_saving_mode_changed(self) -> None:
        """Emit signal that the output saving mode has changed."""
        self.output_saving_mode_changed.emit(self.params.output_saving_mode)

    def _emit_output_path_changed(self) -> None:
        """Emit signal that the output file path has changed."""
        self.output_path_changed.emit(self.params.output_path)
