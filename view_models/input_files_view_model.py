# Coding: UTF-8

# Copyright (C) 2025 Michał Prędki
# Licensed under the GNU General Public License v3.0.
# Full text of the license can be found in the LICENSE file in the repository.

from qgis.PyQt.QtCore import pyqtSignal

from ..dto.data_transfer_objects import InputFilesParams
from .base_view_model import BaseViewModel


class InputFilesViewModel(BaseViewModel):
    """
    ViewModel for managing input file paths and importing datasets.

    This class provides methods and Qt signals to update and track changes
    to the measurements and controls file paths required for data import.
    """

    measurements_file_path_changed = pyqtSignal(str)
    controls_file_path_changed = pyqtSignal(str)

    def __init__(self, model=None) -> None:
        super().__init__()
        self.model = model

        self.params = InputFilesParams()

    def reset_state(self) -> None:
        """Reset the input files parameters and emit signals."""
        self.params = InputFilesParams()
        self._emit_measurements_file_path_changed()
        self._emit_controls_file_path_changed()

    def update_measurements_file_path(self, measurements_file_path: str) -> None:
        """Update the measurements file path and emit the change signal."""
        self.params.measurements_file_path = measurements_file_path
        self._emit_measurements_file_path_changed()

    def update_controls_file_path(self, controls_file_path: str) -> None:
        """Update the controls file path and emit the change signal."""
        self.params.controls_file_path = controls_file_path
        self._emit_controls_file_path_changed()

    def _emit_measurements_file_path_changed(self) -> None:
        """Emit signal that the measurements file path has changed."""
        self.measurements_file_path_changed.emit(self.params.measurements_file_path)

    def _emit_controls_file_path_changed(self) -> None:
        """Emit signal that the controls file path has changed."""
        self.controls_file_path_changed.emit(self.params.controls_file_path)
