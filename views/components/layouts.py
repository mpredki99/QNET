# Coding: UTF-8

# Copyright (C) 2025 Michał Prędki
# Licensed under the GNU General Public License v3.0.
# Full text of the license can be found in the LICENSE file in the repository.

from typing import Optional

from qgis.PyQt.QtWidgets import (
    QCheckBox,
    QComboBox,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
)

from .widgets import QDoubleSpinBoxList


class FileLayout(QFormLayout):
    """
    A form layout for file I/O. Optionally includes a label,
    checkbox, line edit, and button.
    """

    def __init__(
        self,
        label: Optional[QLabel] = None,
        checkbox: Optional[QCheckBox] = None,
        line_edit: Optional[QLineEdit] = None,
        button: Optional[QPushButton] = None,
        parent=None,
    ) -> None:
        super().__init__(parent)

        self.addRow(label)

        row = self._build_file_row(checkbox, line_edit, button)
        self.addRow(row)

    def _build_file_row(
        self,
        checkbox: Optional[QCheckBox],
        line_edit: Optional[QLineEdit],
        button: Optional[QPushButton],
    ) -> QHBoxLayout:
        """Build a horizontal row for file input widgets."""
        file_row_layout = QHBoxLayout()
        if checkbox:
            file_row_layout.addWidget(checkbox, stretch=0)
        if line_edit:
            file_row_layout.addWidget(line_edit, stretch=1)
        if button:
            file_row_layout.addWidget(button, stretch=0)
        return file_row_layout


class WeightingMethodLayout(QFormLayout):
    """
    A form layout for weighting method selection. Supports an optional
    label, checkbox, combo box, and a row of tuning constant spin boxes.
    """

    def __init__(
        self,
        label: Optional[QLabel] = None,
        checkbox: Optional[QCheckBox] = None,
        combo_box: Optional[QComboBox] = None,
        tuning_constants: Optional[QDoubleSpinBoxList] = None,
    ) -> None:
        super().__init__()

        if label:
            self.addRow(label)

        if checkbox is not None and combo_box is not None:
            row = self._build_combo_with_checkbox(checkbox, combo_box)
            self.addRow(row)
        elif combo_box:
            self.addRow(combo_box)

        if tuning_constants:
            row = self._build_tuning_constants_row(tuning_constants)
            self.addRow(row)

    def _build_combo_with_checkbox(
        self, checkbox: QCheckBox, combo_box: QComboBox
    ) -> QHBoxLayout:
        """Build a row with a checkbox and a combo box."""
        combo_box_with_checkbox_layout = QHBoxLayout()
        combo_box_with_checkbox_layout.addWidget(checkbox, stretch=0)
        combo_box_with_checkbox_layout.addWidget(combo_box, stretch=1)
        return combo_box_with_checkbox_layout

    def _build_tuning_constants_row(
        self, tuning_constants: QDoubleSpinBoxList
    ) -> QHBoxLayout:
        """Build a row of tuning constant spin boxes."""
        tuning_constants_layout = QHBoxLayout()
        for spin_box in tuning_constants:
            tuning_constants_layout.addWidget(spin_box)
        return tuning_constants_layout
