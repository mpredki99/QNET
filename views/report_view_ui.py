# Coding: UTF-8

# Copyright (C) 2025 Michał Prędki
# Licensed under the GNU General Public License v3.0.
# Full text of the license can be found in the LICENSE file in the repository.

from qgis.PyQt.QtWidgets import QCheckBox, QLabel, QLineEdit, QPushButton

from .base_view_ui import BaseViewUI
from .components.layouts import FileLayout


class ReportViewUI(BaseViewUI):
    """
    UI base for the report section in the QNET plugin.

    Assembles and configures widgets for selecting report options, such as enabling/disabling
    report generation, specifying the report file name or path, and browsing for a file location.
    """

    def __init__(self) -> None:
        super().__init__()
        self.report_label = QLabel("Report:")
        self.report_checkbox = QCheckBox()
        self.report_line_edit = QLineEdit()
        self.report_button = QPushButton("...")

        layout = self.build_layout()
        self.setLayout(layout)

    def build_layout(self) -> FileLayout:
        """Build and return report file layout."""
        return FileLayout(
            label=self.report_label,
            checkbox=self.report_checkbox,
            line_edit=self.report_line_edit,
            button=self.report_button,
        )
