# Coding: UTF-8

# Copyright (C) 2025 Michał Prędki
# Licensed under the GNU General Public License v3.0.
# Full text of the license can be found in the LICENSE file in the repository.

from typing import Optional

from qgis.PyQt.QtCore import Qt

from ..view_models.report_view_model import ReportViewModel
from .base_views import BaseViewSection
from .components.utils import (
    get_file_path_from_dialog_window,
    update_checkbox_state,
    update_line_edit,
)
from .report_view_ui import ReportViewUI


class ReportView(ReportViewUI, BaseViewSection[ReportViewModel]):
    """
    View class for the report section in the QNET plugin.

    Integrates the UI for report file options with the corresponding view model,
    handling user interactions such as toggling report export, selecting the report
    file path, and updating the UI in response to changes in the view model state.
    """

    file_filter = "Text Files (*.txt)"

    def __init__(self, view_model: Optional[ReportViewModel] = None) -> None:
        super().__init__()
        self.view_model = view_model

    def bind_widgets(self) -> None:
        """Bind UI widgets to their handlers."""
        self.report_button.clicked.connect(self._set_report_path)
        self.report_checkbox.stateChanged.connect(self.view_model.switch_report)
        self.report_line_edit.textChanged.connect(self.view_model.update_report_path)

    def bind_view_model_signals(self) -> None:
        """Bind view model signals to UI update methods."""
        self.view_model.export_report_changed.connect(self.enable_report)
        self.view_model.report_path_changed.connect(self.update_report_line_edit)

    def enable_report(self, enabled: bool) -> None:
        """Enable or disable report control widgets."""
        update_checkbox_state(
            self.report_checkbox, Qt.Checked if enabled else Qt.Unchecked
        )
        self.report_button.setEnabled(enabled)
        self.report_line_edit.setEnabled(enabled)

    def update_report_line_edit(self, new_report_path: str) -> None:
        """Update the report path line edit."""
        update_line_edit(self.report_line_edit, new_report_path)

    def _set_report_path(self) -> None:
        """Open file dialog for report path."""
        path = get_file_path_from_dialog_window(
            self, self.report_label.text()[:-1], "", self.file_filter, "save"
        )
        if path:
            self.view_model.update_report_path(path)
