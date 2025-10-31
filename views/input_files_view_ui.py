# Coding: UTF-8

# Copyright (C) 2025 Michał Prędki
# Licensed under the GNU General Public License v3.0.
# Full text of the license can be found in the LICENSE file in the repository.

from typing import Iterator

from qgis.PyQt.QtWidgets import QLabel, QLineEdit, QPushButton, QVBoxLayout

from .base_views_ui import BaseViewSectionUI
from .components.layouts import FileLayout


class InputFilesViewUI(BaseViewSectionUI):
    """
    UI base for the input files section in the QNET plugin.

    Assembles and configures widgets for selecting measurements and controls input files.
    Provides layouts for file selection fields and buttons.
    """

    def __init__(self) -> None:
        super().__init__()
        self.measurements_label = QLabel("Select measurements.csv file:")
        self.measurements_line_edit = QLineEdit()
        self.measurements_button = QPushButton("...")

        self.controls_label = QLabel("Select controls.csv file:")
        self.controls_line_edit = QLineEdit()
        self.controls_button = QPushButton("...")

        layout = self.build_layout()
        self.setLayout(layout)

    def build_layout(self) -> QVBoxLayout:
        """Build and return the layout for the input files view."""
        main_layout = QVBoxLayout()
        for input_file_layout in self._build_input_file_layouts():
            main_layout.addLayout(input_file_layout)
        return main_layout

    def _build_input_file_layouts(self) -> Iterator[FileLayout]:
        """Yield layouts for input file selection."""
        labels = (self.measurements_label, self.controls_label)
        line_edits = (self.measurements_line_edit, self.controls_line_edit)
        buttons = (self.measurements_button, self.controls_button)

        for label, line_edit, button in zip(labels, line_edits, buttons):
            yield FileLayout(label=label, line_edit=line_edit, button=button)
