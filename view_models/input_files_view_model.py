# Coding: UTF-8

# Copyright (C) 2025 Michał Prędki
# Licensed under the GNU General Public License v3.0.
# Full text of the license can be found in the LICENSE file in the repository.

from qgis.PyQt.QtCore import pyqtSignal

from ..dto.data_transfer_objects import InputFilesParams
from .base_view_models import BaseViewModelSection


class InputFilesViewModel(BaseViewModelSection):
    """
    ViewModel for managing input file paths in QNET plugin.

    This class maintains references to both the `measurements` and `controls`
    datasets.

    Signals
    -------
    - measurements_file_path_changed : pyqtSignal(str)
        Emitted when the measurements file path is updated.
    - controls_file_path_changed : pyqtSignal(str)
        Emitted when the controls file path is updated.

    Attributes
    ----------
    - params : InputFilesParams
        Data transfer object containing the current input file paths.
    """

    measurements_file_path_changed = pyqtSignal(str)
    controls_file_path_changed = pyqtSignal(str)

    def __init__(self) -> None:
        """Initialize the ViewModel with default input file parameters."""
        super().__init__()
        self.params = InputFilesParams()

    def reset_state(self) -> None:
        """Reset all input file parameters to defaults and emit signals."""
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
        """Emit the measurements file path changed signal."""
        self.measurements_file_path_changed.emit(self.params.measurements_file_path)

    def _emit_controls_file_path_changed(self) -> None:
        """Emit the controls file path changed signal."""
        self.controls_file_path_changed.emit(self.params.controls_file_path)
