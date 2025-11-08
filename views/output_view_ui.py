# Coding: UTF-8

# Copyright (C) 2025 Michał Prędki
# Licensed under the GNU General Public License v3.0.
# Full text of the license can be found in the LICENSE file in the repository.

from qgis.PyQt.QtWidgets import QLabel, QLineEdit, QPushButton

from .base_views_ui import BaseViewSectionUI
from .components.layouts import FileLayout
from .components.widgets import SavingModeMenu


class OutputViewUI(BaseViewSectionUI):
    """
    UI base class for the Output section in the QNET plugin.

    This class defines and arranges the widgets used for selecting the output file
    location and configuring how results are saved. It provides a labeled input field
    for specifying the output path, a menu-enabled button for choosing saving modes.

    Attributes
    ----------
    - output_label : QLabel
        Label for the output file path.
    - output_line_edit : QLineEdit
        Text input field for specifying the QGIS layer output file path.
    - output_button : QPushButton
        Button for selecting file saving mode.
    - output_saving_mode_menu : SavingModeMenu
        Menu widget providing options for selecting the output saving mode.
    """

    def __init__(self) -> None:
        """Initialize all widgets used for the section View."""
        super().__init__()
        self.output_label = QLabel("Select output path:")
        self.output_line_edit = QLineEdit()
        self.output_button = QPushButton("...")
        self.output_saving_mode_menu = SavingModeMenu()

        layout = self.build_layout()
        self.setLayout(layout)

    def build_layout(self) -> FileLayout:
        self._configure_widgets()
        """Build and return the layout for the output file section."""
        return FileLayout(
            label=self.output_label,
            line_edit=self.output_line_edit,
            button=self.output_button,
        )

    def _configure_widgets(self) -> None:
        """Configure widgets for output file section"""
        self.output_line_edit.setPlaceholderText("[Temporary layer]")
        self.output_button.setMenu(self.output_saving_mode_menu)
