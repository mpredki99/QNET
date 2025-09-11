# Coding: UTF-8

# Copyright (C) 2025 Michał Prędki
# Licensed under the GNU General Public License v3.0.
# Full text of the license can be found in the LICENSE file in the repository.

from functools import partial
from itertools import zip_longest
from typing import List, Tuple

from qgis.PyQt.QtWidgets import (
    QAction,
    QComboBox,
    QDoubleSpinBox,
    QFileDialog,
    QLineEdit,
)

from ..infrastructure import WEIGHTING_METHODS, get_default_tuning_constants
from .main_view_ui import MainViewUI


class MainView(MainViewUI):
    def __init__(self, view_model=None) -> None:
        super().__init__()

        self.view_model = view_model
        self.output_saving_mode = "temp_layer"
        self._populate_output_menu()
        self._bind_widgets()

    def set_input_file(self, line_edit: QLineEdit, window_title: str) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self, window_title, "", "CSV Files (*.csv)"
        )
        if path:
            line_edit.setText(path)

    def switch_free_adjustment(self, state: int) -> None:
        is_enabled = state == 2
        self.free_adjustment_weighting_method_combo_box.setEnabled(is_enabled)
        self.set_enabled_free_adjustment_weighting_method_tuning_constants(is_enabled)

    def set_enabled_free_adjustment_weighting_method_tuning_constants(
        self, is_enabled: bool
    ) -> None:
        for spin_box in self.free_adjustment_weighting_method_tuning_constants:
            spin_box.setEnabled(is_enabled)

    def weighting_method_changed(
        self, combo_box: QComboBox, tuning_constants_list: List[QDoubleSpinBox]
    ) -> None:
        weighting_method = WEIGHTING_METHODS[combo_box.currentText()]
        tuning_constant_values = get_default_tuning_constants(weighting_method)
        self.refresh_tuning_constant_spin_boxes(
            tuning_constant_values, tuning_constants_list
        )

    def refresh_tuning_constant_spin_boxes(
        self,
        tuning_constant_values: Tuple[float],
        tuning_constants_list: List[QDoubleSpinBox],
    ) -> None:
        for spin_box, c in zip_longest(
            tuning_constants_list, tuning_constant_values, fillvalue=None
        ):
            (spin_box.setValue(c), spin_box.show()) if c else spin_box.hide()

    def switch_report(self, state: int) -> None:
        is_enabled = state == 2
        self.report_button.setEnabled(is_enabled)
        self.report_line_edit.setEnabled(is_enabled)

    def set_report_path(self) -> None:
        path, _ = QFileDialog.getSaveFileName(
            self, "Save report", "", "Text Files (*.txt)"
        )
        if path:
            self.report_line_edit.setText(path)

    def set_output_mode(self, mode: str) -> None:
        if mode == "temp_layer" and self.output_saving_mode != "temp_layer":
            self.output_saving_mode = mode
            self.output_line_edit.setText("")

        elif mode == "to_file":
            self.output_saving_mode = mode
            self.set_output_path()

    def set_output_path(self) -> None:
        path, _ = QFileDialog.getSaveFileName(
            self, "Select output file", "", "Shapefile (*.shp)"
        )
        if path:
            self.output_line_edit.setText(path)

    def perform_adjustment(self) -> None:
        # TODO: Pass the adjustment parameters to the view model command
        print("----- PERFORM ADJUSTMENT -----")
        print()

        print("----- Input files -----")
        print("measurements.csv:", self.measurements_line_edit.text())
        print("controls.csv", self.controls_line_edit.text())
        print()

        print("----- Weighting methods -----")
        print(
            "Observations:", self.observation_weighting_method_combo_box.currentText()
        )
        for i, obs_c in enumerate(self.observation_weighting_method_tuning_constants):
            if obs_c.isHidden():
                break
            print(f"c_{i+1}:", obs_c.value())
        print()

        if self.free_adjustment_weighting_method_combo_box.isEnabled():
            print(
                "Free adjustment:",
                self.free_adjustment_weighting_method_combo_box.currentText(),
            )
        for i, obs_c in enumerate(
            self.free_adjustment_weighting_method_tuning_constants
        ):
            if obs_c.isHidden():
                break
            print(f"c_{i+1}:", obs_c.value())
        print()

        if self.report_line_edit.isEnabled():
            print("----- Export report -----")
            print("Report path:", self.report_line_edit.text())
        print()

        print("----- Output -----")
        print("Output_mode:", self.output_saving_mode)
        if self.output_saving_mode == "temp_layer":
            print("Temp layer name", self.output_line_edit.text())
        else:
            print("Output file path:", self.output_line_edit.text())

    # ====================================================
    def _populate_output_menu(self):
        qmenu_actions = self._define_output_mode_actions()
        for action in qmenu_actions:
            self.output_saving_mode_menu.addAction(action)

    def _define_output_mode_actions(self):
        temp_layer_mode_action = self._define_output_mode_action(
            "temp_layer", "Temporary layer"
        )
        to_file_mode_action = self._define_output_mode_action("to_file", "To file")

        return temp_layer_mode_action, to_file_mode_action

    def _define_output_mode_action(self, action_mode: str, action_name: str):
        action = QAction(action_name, self)
        action.triggered.connect(lambda: self.set_output_mode(action_mode))

        return action

    def _bind_widgets(self):
        self._bind_input_file_buttons()
        self._bind_weighting_method_combo_boxes()
        self.free_adjustment_checkbox.stateChanged.connect(self.switch_free_adjustment)
        self.report_checkbox.stateChanged.connect(self.switch_report)
        self.report_button.clicked.connect(self.set_report_path)
        self.ok_button.clicked.connect(self.perform_adjustment)

    def _bind_input_file_buttons(self) -> None:
        buttons = (self.measurements_button, self.controls_button)
        line_edits = (self.measurements_line_edit, self.controls_line_edit)
        labels = (self.measurements_label, self.controls_label)

        for button, line_edit, label in zip(buttons, line_edits, labels):
            window_label = label.text()[:-1]
            button.clicked.connect(
                partial(self.set_input_file, line_edit, window_label)
            )

    def _bind_weighting_method_combo_boxes(self):
        combo_boxes = (
            self.observation_weighting_method_combo_box,
            self.free_adjustment_weighting_method_combo_box,
        )
        tuning_constant_lists = (
            self.observation_weighting_method_tuning_constants,
            self.free_adjustment_weighting_method_tuning_constants,
        )

        for combo_box, tuning_constants_list in zip(combo_boxes, tuning_constant_lists):
            combo_box.currentIndexChanged.connect(
                partial(self.weighting_method_changed, combo_box, tuning_constants_list)
            )
