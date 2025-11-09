# Coding: UTF-8

# Copyright (C) 2025 Michał Prędki
# Licensed under the GNU General Public License v3.0.
# Full text of the license can be found in the LICENSE file in the repository.

from qgis.PyQt.QtCore import pyqtSignal

from ..dto.data_transfer_objects import ReportParams
from .base_view_models import BaseViewModelSection


class ReportViewModel(BaseViewModelSection):
    """
    ViewModel for managing report export options.

    This class is responsible for managing the report export option (on/off) and the file path
    where the report is saved. It also emits a signal if report export is enabled but no
    path has been specified.

    Signals
    -------
    - export_report_changed : pyqtSignal(bool)
        Emitted when the report export toggle state changes.
    - report_path_changed : pyqtSignal(str)
        Emitted when the report file path changes.
    - missing_report_path : pyqtSignal()
        Emitted when a report export is attempted without a file path defined.

    Attributes
    ----------
    - params : ReportParams
        Data transfer object storing the report export options.
    """

    export_report_changed = pyqtSignal(bool)
    report_path_changed = pyqtSignal(str)

    missing_report_path = pyqtSignal()

    def __init__(self) -> None:
        """Initialize the ViewModel with default report parameters."""
        super().__init__()
        self.params = ReportParams()

    def reset_state(self) -> None:
        """Reset all report parameters to defaults and emit signals."""
        self.params = ReportParams()
        self._emit_export_report_changed()
        self._emit_report_path_changed()

    def switch_report(self, state: int) -> None:
        """Toggle report export on or off based on the given state."""
        self.params.export_report = state == 2
        self._emit_export_report_changed()

    def update_report_path(self, report_path: str) -> None:
        """Update the report file path and emit a change signal."""
        self.params.report_path = report_path
        self._emit_report_path_changed()

    def _emit_export_report_changed(self) -> None:
        """Emit export report changed signal."""
        self.export_report_changed.emit(self.params.export_report)

    def _emit_report_path_changed(self) -> None:
        """Emit report path changed signal."""
        self.report_path_changed.emit(self.params.report_path)
