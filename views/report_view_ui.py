# Coding: UTF-8

# Copyright (C) 2025 Michał Prędki
# Licensed under the GNU General Public License v3.0.
# Full text of the license can be found in the LICENSE file in the repository.

from qgis.PyQt.QtWidgets import QCheckBox, QLabel, QLineEdit, QPushButton

from .base_views_ui import BaseViewSectionUI
from .components.layouts import FileLayout


class ReportViewUI(BaseViewSectionUI):
    """
    UI base class for the Report export section in the QNET plugin.

    This class defines and organizes the user interface elements related to report
    generation. It provides widgets for enabling or disabling report creation, 
    specifying the output report file path, and browsing for a destination file. 

    Attributes
    ----------
    - report_label : QLabel
        Label for export report section.
    - report_checkbox : QCheckBox
        Checkbox enabling or disabling report generation.
    - report_line_edit : QLineEdit
        Text input field for specifying the report file path.
    - report_button : QPushButton
        Button opening a file dialog for selecting the report file location.
    """


    def __init__(self) -> None:
        """Initialize all widgets used for the export report section View."""
        super().__init__()
        self.report_label = QLabel("Report:")
        self.report_checkbox = QCheckBox()
        self.report_line_edit = QLineEdit()
        self.report_button = QPushButton("...")

        layout = self.build_layout()
        self.setLayout(layout)

    def build_layout(self) -> FileLayout:
        """Build and return main layout containing all section widgets."""
        return FileLayout(
            label=self.report_label,
            checkbox=self.report_checkbox,
            line_edit=self.report_line_edit,
            button=self.report_button,
        )
