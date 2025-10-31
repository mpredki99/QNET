# Coding: UTF-8

# Copyright (C) 2025 Michał Prędki
# Licensed under the GNU General Public License v3.0.
# Full text of the license can be found in the LICENSE file in the repository.

from qgis.PyQt.QtWidgets import QPushButton, QVBoxLayout

from .base_views_ui import BaseViewUI
from .input_files_view import InputFilesView
from .output_view import OutputView
from .report_view import ReportView
from .weighting_methods_view import WeightingMethodsView


class MainViewUI(BaseViewUI):
    """
    Main dialog UI for the QNET plugin.

    Assembles and configures all widgets and layouts for file selection,
    weighting method configuration, report options, and output settings.
    """

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("QNET")
        self.resize(430, 285)

        layout = self.build_layout()
        self.setLayout(layout)

    def build_layout(self):
        layout = QVBoxLayout()

        self.input_file_view = InputFilesView()
        self.weighting_methods_view = WeightingMethodsView()
        self.report_view = ReportView()
        self.output_view = OutputView()
        self.ok_button = QPushButton("OK")

        layout.addWidget(self.input_file_view)
        layout.addWidget(self.weighting_methods_view)
        layout.addWidget(self.report_view)
        layout.addWidget(self.output_view)
        layout.addSpacing(10)
        layout.addWidget(self.ok_button)

        return layout
