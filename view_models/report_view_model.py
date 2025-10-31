# Coding: UTF-8

# Copyright (C) 2025 Michał Prędki
# Licensed under the GNU General Public License v3.0.
# Full text of the license can be found in the LICENSE file in the repository.

from qgis.PyQt.QtCore import pyqtSignal

from ..dto.data_transfer_objects import ReportParams
from .base_view_models import BaseViewModelSection


class ReportViewModel(BaseViewModelSection):
    """
    ViewModel for managing report export options and state in the QNET plugin.

    This class encapsulates the logic and state for report file export, including
    enabling/disabling report generation, storing the report file path, and emitting
    Qt signals when these values change. It interacts with the ExportReportCommand to
    handle the export process and notifies the UI if a required report path is missing.
    """

    export_report_changed = pyqtSignal(bool)
    repot_path_changed = pyqtSignal(str)

    missing_report_path = pyqtSignal()

    def __init__(self, model=None) -> None:
        super().__init__()
        self.model = model

        self.params = ReportParams()

    def reset_state(self) -> None:
        """Reset report parameters and emit signals."""
        self.params = ReportParams()
        self._emit_export_report_changed()
        self._emit_report_path_changed()

    def switch_report(self, state: int) -> None:
        """Switch the export report state in report params."""
        self.params.export_report = state == 2
        self._emit_export_report_changed()

    def update_report_path(self, report_path: str) -> None:
        """Update the report file path and emit changed signal."""
        self.params.report_path = report_path
        self._emit_report_path_changed()

    def _emit_export_report_changed(self) -> None:
        """Emit export_report_changed signal."""
        self.export_report_changed.emit(self.params.export_report)

    def _emit_report_path_changed(self) -> None:
        """Emit report_path_changed signal."""
        self.repot_path_changed.emit(self.params.report_path)
