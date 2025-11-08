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

    Serves as the top-level user interface container that assembles all major sections 
    of the QNET plugin, including input file selection, weighting method configuration, 
    report settings, and output management. This class is responsible for initializing
    and arranging all section views in a dialog layout.
    
    Attributes
    ----------
    - input_file_view : InputFilesView
        Widget section for selecting measurement and control input files.
    - weighting_methods_view : WeightingMethodsView
        Widget section for configuring observation and free adjustment weighting methods.
    - report_view : ReportView
        Widget section for managing report generation and output path.
    - output_view : OutputView
        Widget section for defining QGIS layer output file path and saving options.
    - ok_button : QPushButton
        Button used to confirm and execute the calculations.
    """

    def __init__(self) -> None:
        """Initialize all widgets and sub-views for main view UI."""
        super().__init__()
        self.setWindowTitle("QNET")
        self.resize(430, 285)
        
        self.input_file_view = InputFilesView()
        self.weighting_methods_view = WeightingMethodsView()
        self.report_view = ReportView()
        self.output_view = OutputView()
        self.ok_button = QPushButton("OK")

        layout = self.build_layout()
        self.setLayout(layout)

    def build_layout(self) -> QVBoxLayout:
        """Build and return the main layout containing all section sub-views."""
        layout = QVBoxLayout()

        layout.addWidget(self.input_file_view)
        layout.addWidget(self.weighting_methods_view)
        layout.addWidget(self.report_view)
        layout.addWidget(self.output_view)
        layout.addSpacing(10)
        layout.addWidget(self.ok_button)

        return layout
