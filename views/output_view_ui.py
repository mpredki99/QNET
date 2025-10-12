# Coding: UTF-8

# Copyright (C) 2025 Michał Prędki
# Licensed under the GNU General Public License v3.0.
# Full text of the license can be found in the LICENSE file in the repository.

from typing import Iterator

from qgis.PyQt.QtWidgets import QLabel, QLineEdit, QPushButton, QVBoxLayout

from .base_view_ui import BaseViewUI
from .components.layouts import FileLayout
from .components.widgets import SavingModeMenu


class OutputViewUI(BaseViewUI):
    """
    UI base for the output section in the QNET plugin.

    Assembles and configures widgets for selecting the output file path and choosing the output
    saving mode. Provides the layout for the output path field, menu button, and label.
    """

    def __init__(self) -> None:
        super().__init__()
        self.output_label = QLabel("Select output path:")
        self.output_line_edit = QLineEdit()
        self.output_button = QPushButton("...")
        self.output_saving_mode_menu = SavingModeMenu()

        self.output_line_edit.setPlaceholderText("[Temporary layer]")
        self.output_button.setMenu(self.output_saving_mode_menu)

        layout = self.build_layout()
        self.setLayout(layout)

    def build_layout(self) -> FileLayout:
        """Build and return output file layout."""
        return FileLayout(
            label=self.output_label,
            line_edit=self.output_line_edit,
            button=self.output_button,
        )
