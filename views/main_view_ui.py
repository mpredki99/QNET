# Coding: UTF-8

# Copyright (C) 2025 Michał Prędki
# Licensed under the GNU General Public License v3.0.
# Full text of the license can be found in the LICENSE file in the repository.

from typing import List

from qgis.PyQt.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QDoubleSpinBox,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMenu,
    QPushButton,
    QVBoxLayout,
)

from ..infrastructure.weighting_methods import WEIGHTING_METHODS


class MainViewUI(QDialog):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("QNET")
        self.resize(430, 285)

        # Initialize view widgets
        self.measurements_label = QLabel("Select measurements.csv file:")
        self.measurements_line_edit = QLineEdit()
        self.measurements_button = QPushButton("...")

        self.controls_label = QLabel("Select controls.csv file:")
        self.controls_line_edit = QLineEdit()
        self.controls_button = QPushButton("...")

        self.observation_weighting_method_label = QLabel(
            "Observations weighting methods"
        )
        self.observation_weighting_method_combo_box = QComboBox()
        self.observation_weighting_method_tuning_constants = (
            self._get_tuning_constants_spinbox_list()
        )

        self.free_adjustment_weighting_method_label = QLabel(
            "Free adjustment weighting methods"
        )
        self.free_adjustment_checkbox = QCheckBox()
        self.free_adjustment_weighting_method_combo_box = QComboBox()
        self.free_adjustment_weighting_method_tuning_constants = (
            self._get_tuning_constants_spinbox_list()
        )

        self.report_label = QLabel("Report:")
        self.report_checkbox = QCheckBox()
        self.report_line_edit = QLineEdit()
        self.report_button = QPushButton("...")

        self.output_label = QLabel("Select output path:")
        self.output_line_edit = QLineEdit()
        self.output_button = QPushButton("...")
        self.output_saving_mode_menu = QMenu()

        self.ok_button = QPushButton("OK")

        main_layout = self._build_main_layout()
        self.setLayout(main_layout)

    def _get_tuning_constants_spinbox_list(self) -> List[QDoubleSpinBox]:
        return [QDoubleSpinBox() for _ in range(3)]

    def _build_main_layout(self) -> QVBoxLayout:
        input_files_layout = self._build_input_files_layout()
        weighting_methods_layout = self._build_weighting_methods_layout()
        report_layout = self._build_report_layout()
        output_layout = self._build_output_layout()

        main_layout = QVBoxLayout()
        main_layout.addLayout(input_files_layout)
        main_layout.addLayout(weighting_methods_layout)
        main_layout.addLayout(report_layout)
        main_layout.addLayout(output_layout)
        main_layout.addWidget(self.ok_button)
        return main_layout

    # Input files layout ==================================================
    def _build_input_files_layout(self) -> QFormLayout:
        labels = (self.measurements_label, self.controls_label)
        line_edits = (self.measurements_line_edit, self.controls_line_edit)
        buttons = (self.measurements_button, self.controls_button)

        input_files_form_layout = QFormLayout()
        for label, line_edit, button in zip(labels, line_edits, buttons):
            input_file_layout = self._build_input_file_layout(line_edit, button)
            input_files_form_layout.addRow(label)
            input_files_form_layout.addRow(input_file_layout)

        return input_files_form_layout

    def _build_input_file_layout(
        self, line_edit: QLineEdit, button: QPushButton
    ) -> QHBoxLayout:
        input_file_layout = QHBoxLayout()
        input_file_layout.addWidget(line_edit, stretch=1)
        input_file_layout.addWidget(button, stretch=0)

        return input_file_layout

    # Weighting methods layout ==================================================
    def _build_weighting_methods_layout(self) -> QFormLayout:
        weighting_methods_row_layout = self._build_weighting_methods_row_layout()

        weighting_methods_form_layout = QFormLayout()
        weighting_methods_form_layout.addRow(weighting_methods_row_layout)

        return weighting_methods_form_layout

    def _build_weighting_methods_row_layout(self) -> QHBoxLayout:
        observation_weighting_methods_layout = (
            self._build_observation_weighting_methods_layout()
        )
        free_adjustment_weighting_methods_layout = (
            self._build_free_adjustment_weighting_methods_layout()
        )

        weighting_methods_row_layout = QHBoxLayout()
        weighting_methods_row_layout.addLayout(
            observation_weighting_methods_layout, stretch=1
        )
        weighting_methods_row_layout.addLayout(
            free_adjustment_weighting_methods_layout, stretch=1
        )

        return weighting_methods_row_layout

    def _build_observation_weighting_methods_layout(self) -> QFormLayout:
        self._populate_weighting_methods_combo_box(
            self.observation_weighting_method_combo_box
        )
        observation_tuning_constants_layout = self._build_tuning_constants_layout(
            self.observation_weighting_method_tuning_constants
        )

        observation_weighting_method_layout = QFormLayout()
        observation_weighting_method_layout.addRow(
            self.observation_weighting_method_label
        )
        observation_weighting_method_layout.addRow(
            self.observation_weighting_method_combo_box
        )
        observation_weighting_method_layout.addRow(observation_tuning_constants_layout)

        return observation_weighting_method_layout

    def _build_free_adjustment_weighting_methods_layout(self) -> QFormLayout:
        self._configure_free_adjustment_weighting_methods_layout_widgets()
        weighting_methods_combo_box_layout = (
            self._build_weighting_methods_combo_box_layout()
        )
        free_adjustment_tuning_constants_layout = self._build_tuning_constants_layout(
            self.free_adjustment_weighting_method_tuning_constants
        )

        free_adjustment_weighting_methods_layout = QFormLayout()
        free_adjustment_weighting_methods_layout.addRow(
            self.free_adjustment_weighting_method_label
        )
        free_adjustment_weighting_methods_layout.addRow(
            weighting_methods_combo_box_layout
        )
        free_adjustment_weighting_methods_layout.addRow(
            free_adjustment_tuning_constants_layout
        )

        return free_adjustment_weighting_methods_layout

    def _configure_free_adjustment_weighting_methods_layout_widgets(self) -> None:
        self._populate_weighting_methods_combo_box(
            self.free_adjustment_weighting_method_combo_box
        )
        self.free_adjustment_weighting_method_combo_box.setEnabled(False)

    def _populate_weighting_methods_combo_box(
        self, weighting_methods_combo_box
    ) -> None:
        weighting_methods_combo_box.addItems(
            [label for label in WEIGHTING_METHODS.keys()]
        )

    def _build_weighting_methods_combo_box_layout(self) -> QHBoxLayout:
        weighting_methods_combo_box_layout = QHBoxLayout()
        weighting_methods_combo_box_layout.addWidget(
            self.free_adjustment_checkbox, stretch=0
        )
        weighting_methods_combo_box_layout.addWidget(
            self.free_adjustment_weighting_method_combo_box, stretch=1
        )

        return weighting_methods_combo_box_layout

    def _build_tuning_constants_layout(
        self, tuning_constants_spin_box_list: List[QDoubleSpinBox]
    ) -> QHBoxLayout:
        tuning_constants_layout = QHBoxLayout()

        for spin_box in tuning_constants_spin_box_list:
            self._configure_tuning_constant_spin_box(spin_box)
            tuning_constants_layout.addWidget(spin_box)

        return tuning_constants_layout

    def _configure_tuning_constant_spin_box(self, spin_box: QDoubleSpinBox) -> None:
        spin_box.setDecimals(3)
        spin_box.setRange(0, 100.0)
        spin_box.setSingleStep(0.01)
        spin_box.hide()

    # Report layout ===================================================
    def _build_report_layout(self) -> QFormLayout:
        self._configure_report_layout_widgets()
        report_line_edit_layout = self._build_report_line_edit_layout()

        report_form_layout = QFormLayout()
        report_form_layout.addRow(self.report_label)
        report_form_layout.addRow(report_line_edit_layout)

        return report_form_layout

    def _configure_report_layout_widgets(self) -> None:
        self.report_line_edit.setEnabled(False)
        self.report_button.setEnabled(False)

    def _build_report_line_edit_layout(self) -> QHBoxLayout:
        report_line_edit_layout = QHBoxLayout()
        report_line_edit_layout.addWidget(self.report_checkbox, stretch=0)
        report_line_edit_layout.addWidget(self.report_line_edit, stretch=1)
        report_line_edit_layout.addWidget(self.report_button, stretch=0)

        return report_line_edit_layout

    # Output layout ===================================================
    def _build_output_layout(self) -> QFormLayout:
        self._configure_output_layout_widgets()
        output_line_edit_layout = self._build_output_line_edit_layout()

        output_form_layout = QFormLayout()
        output_form_layout.addRow(self.output_label)
        output_form_layout.addRow(output_line_edit_layout)

        return output_form_layout

    def _configure_output_layout_widgets(self) -> None:
        self.output_line_edit.setPlaceholderText("[Temporary layer]")
        self.output_button.setMenu(self.output_saving_mode_menu)

    def _build_output_line_edit_layout(self) -> QHBoxLayout:
        output_line_edit_layout = QHBoxLayout()
        output_line_edit_layout.addWidget(self.output_line_edit)
        output_line_edit_layout.addWidget(self.output_button)

        return output_line_edit_layout
