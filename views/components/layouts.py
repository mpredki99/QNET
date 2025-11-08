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
    Standardized form layout for file input and output widgets.

    Provides a flexible layout for combining common file selection controls
    such as a label, optional enable/disable checkbox, line edit for path display,
    and a button for browsing or saving files.
    """

    def __init__(
        self,
        label: Optional[QLabel] = None,
        checkbox: Optional[QCheckBox] = None,
        line_edit: Optional[QLineEdit] = None,
        button: Optional[QPushButton] = None,
        parent=None,
    ) -> None:
        """
        Initialize FileLayout object.
        
        Parameters
        ----------
        - label : QLabel, optional
            Descriptive label for the file input section.
        - checkbox : QCheckBox, optional
            Checkbox to enable or disable file-related options.
        - line_edit : QLineEdit, optional
            Line edit for displaying or manually entering the file path.
        - button : QPushButton, optional
            Button for invoking a file dialog or confirming file selection.
        - parent : QWidget, optional
            Parent widget for the layout.
        """
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
        """Build a horizontal layout row for the checkbox, line edit, and button."""
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
    Form layout for configuring weighting methods.

    Assembles widgets related to weighting method selection, including an
    optional label, checkbox, combo box for choosing the method, and a row
    of QDoubleSpinBox widgets for entering method-specific tuning constants.
    """

    def __init__(
        self,
        label: Optional[QLabel] = None,
        checkbox: Optional[QCheckBox] = None,
        combo_box: Optional[QComboBox] = None,
        tuning_constants: Optional[QDoubleSpinBoxList] = None,
    ) -> None:
        """
        Initialize WeightingMethodLayout.
        
        Parameters
        ----------
        - label : QLabel, optional
            Label describing the weighting method section.
        - checkbox : QCheckBox, optional
            Checkbox to enable or disable weighting method configuration.
        - combo_box : QComboBox, optional
            Combo box listing available weighting methods.
        - tuning_constants : QDoubleSpinBoxList, optional
            Container holding spin boxes for tuning constants.
        """
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
