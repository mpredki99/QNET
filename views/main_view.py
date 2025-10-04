# Coding: UTF-8

# Copyright (C) 2025 Michał Prędki
# Licensed under the GNU General Public License v3.0.
# Full text of the license can be found in the LICENSE file in the repository.

from functools import partial
from itertools import zip_longest
from typing import Tuple

from qgis.PyQt.QtWidgets import QComboBox, QFileDialog, QLineEdit

from ..dto.data_transfer_objects import (
    AdjustmentParams,
    OutputParams,
    ReaderParams,
    ReportParams,
)
from ..infrastructure import WEIGHTING_METHODS, get_default_tuning_constants
from .components.widgets import QDoubleSpinBoxList
from .main_view_ui import MainViewUI


class MainView(MainViewUI):
    """
    Main dialog logic for the QNET plugin.

    Handles user interactions, file selection, weighting method configuration,
    report and output options, and binds UI events to logic.
    """

    input_file_filter = "CSV Files (*.csv)"
    report_file_filter = "Text Files (*.txt)"
    output_file_filter = "Shapefile (*.shp)"

    def __init__(self, view_model=None) -> None:
        super().__init__()

        self.view_model = view_model
        self.output_saving_mode = "Temporary layer"
        self._bind_widgets()

    def set_input_file(self, line_edit: QLineEdit, window_title: str) -> None:
        """Open file dialog and set selected file path to the line edit."""
        path, _ = QFileDialog.getOpenFileName(
            self, window_title, "", self.input_file_filter
        )
        if path:
            line_edit.setText(path)

    def switch_free_adjustment(self, state: int) -> None:
        """Enable or disable free adjustment weighting method controls."""
        is_enabled = state == 2
        self.free_adjustment_weighting_method_combo_box.setEnabled(is_enabled)
        self.free_adjustment_weighting_method_tuning_constants.setEnabled(is_enabled)

    def weighting_method_changed(
        self, combo_box: QComboBox, tuning_constants_list: QDoubleSpinBoxList
    ) -> None:
        """Update tuning constant spin boxes when weighting method changes."""
        weighting_method = WEIGHTING_METHODS[combo_box.currentText()]
        tuning_constants = get_default_tuning_constants(weighting_method)
        self._refresh_tuning_constant_spin_boxes(
            tuning_constants.values(), tuning_constants_list
        )

    def switch_report(self, state: int) -> None:
        """Enable or disable report file controls."""
        is_enabled = state == 2
        self.report_button.setEnabled(is_enabled)
        self.report_line_edit.setEnabled(is_enabled)

    def set_report_path(self) -> None:
        """Open file dialog to select report file path."""
        path, _ = QFileDialog.getSaveFileName(
            self, "Save report", "", self.report_file_filter
        )
        if path:
            self.report_line_edit.setText(path)

    def set_output_mode(self, output_mode: str) -> None:
        """Set the output saving mode and handle output path if needed."""
        output_handlers = {
            "Temporary layer": partial(self._handle_temporary_output, output_mode),
            "To file": partial(self._handle_file_output, output_mode),
        }

        output_handler = output_handlers.get(output_mode)
        if output_handler:
            output_handler()

    def perform_adjustment(self) -> None:
        """Perform the adjustment using parameters from the UI."""
        reader_params = self._get_reader_params()
        adjustment_params = self._get_adjustment_params()
        report_params = self._get_report_params()
        output_params = self._get_output_params()

        self.view_model.perform_adjustment(
            reader_params, adjustment_params, report_params, output_params
        )

    def _refresh_tuning_constant_spin_boxes(
        self,
        tuning_constants_values: Tuple[float],
        tuning_constants_list: QDoubleSpinBoxList,
    ) -> None:
        """Update and show/hide tuning constant spin boxes based on method."""
        for spin_box, c in zip_longest(
            tuning_constants_list, tuning_constants_values, fillvalue=None
        ):
            (spin_box.setValue(c), spin_box.show()) if c else spin_box.hide()

    def _handle_temporary_output(self, output_mode: str):
        """Handle output mode when 'Temporary layer' is selected."""
        if self.output_saving_mode != "Temporary layer":
            self.output_saving_mode = output_mode
            self.output_line_edit.setText("")

    def _handle_file_output(self, output_mode: str):
        """Handle output mode when 'To file' is selected."""
        self.output_saving_mode = output_mode
        self._set_output_path()

    def _set_output_path(self) -> None:
        """Open file dialog to select output file path."""
        path, _ = QFileDialog.getSaveFileName(
            self, "Select output file", "", self.output_file_filter
        )
        if path:
            self.output_line_edit.setText(path)

    def _bind_widgets(self):
        """Bind all widget signals to their respective handlers."""
        self._bind_input_file_buttons()
        self._bind_weighting_method_combo_boxes()
        self.free_adjustment_checkbox.stateChanged.connect(self.switch_free_adjustment)
        self.report_checkbox.stateChanged.connect(self.switch_report)
        self.report_button.clicked.connect(self.set_report_path)
        self._bind_output_saving_mode_menu()
        self.ok_button.clicked.connect(self.perform_adjustment)

    def _bind_input_file_buttons(self) -> None:
        """Bind input file buttons to open file dialogs."""
        buttons = (self.measurements_button, self.controls_button)
        line_edits = (self.measurements_line_edit, self.controls_line_edit)
        labels = (self.measurements_label, self.controls_label)

        for button, line_edit, label in zip(buttons, line_edits, labels):
            window_label = label.text()[:-1]
            button.clicked.connect(
                partial(self.set_input_file, line_edit, window_label)
            )

    def _bind_weighting_method_combo_boxes(self):
        """Bind weighting method combo boxes to update tuning constants."""
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

    def _bind_output_saving_mode_menu(self):
        """Bind output saving mode menu actions to set output mode."""
        for action in self.output_saving_mode_menu.actions():
            action.triggered.connect(partial(self.set_output_mode, action.text()))

    def _get_reader_params(self):
        """Get reader parameters from the UI."""
        return ReaderParams(
            measurements_file_path=self.measurements_line_edit.text(),
            controls_file_path=self.controls_line_edit.text(),
        )

    def _get_adjustment_params(self):
        """Get adjustment parameters from the UI."""
        obs_adj = self.observation_weighting_method_combo_box.currentText()
        free_adjustment = (
            self.free_adjustment_weighting_method_combo_box.currentText()
            if self.free_adjustment_weighting_method_combo_box.isEnabled()
            else None
        )
        return AdjustmentParams(
            obs_adj=obs_adj,
            obs_tuning_constants=self._get_tuning_constants_from_user(
                obs_adj, self.observation_weighting_method_tuning_constants
            ),
            free_adjustment=free_adjustment,
            free_adj_tuning_constants=self._get_tuning_constants_from_user(
                free_adjustment, self.free_adjustment_weighting_method_tuning_constants
            ),
        )

    def _get_report_params(self):
        """Get report parameters from the UI."""
        return ReportParams(
            report_path=(
                self.report_line_edit.text()
                if self.report_line_edit.isEnabled()
                else None
            ),
        )

    def _get_output_params(self):
        """Get output parameters from the UI."""
        return OutputParams(
            output_saving_mode=self.output_saving_mode,
            output_path=(
                self.output_line_edit.text() if self.output_line_edit.text() else None
            ),
        )
        
    def _get_tuning_constants_from_user(
        self, method: str, tuning_constants_list: QDoubleSpinBoxList
    ) -> dict:
        """Get tuning constants from user input."""
        if not method:
            return

        tuning_constants = get_default_tuning_constants(WEIGHTING_METHODS[method])
        for key, spin_box in zip(tuning_constants.keys(), tuning_constants_list):
            if spin_box.isHidden():
                break
            tuning_constants[key] = spin_box.value()
        return tuning_constants
