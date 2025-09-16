# Coding: UTF-8

# Copyright (C) 2025 Michał Prędki
# Licensed under the GNU General Public License v3.0.
# Full text of the license can be found in the LICENSE file in the repository.

from qgis.PyQt.QtWidgets import (
    QCheckBox,
    QDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
)

from .components.layouts import FileLayout, WeightingMethodLayout
from .components.widgets import (
    QDoubleSpinBoxList,
    SavingModeMenu,
    WeightingMethodComboBox,
)


class MainViewUI(QDialog):
    """
    Main dialog UI for the QNET plugin.

    Assembles and configures all widgets and layouts for file selection,
    weighting method configuration, report options, and output settings.
    """

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
        self.observation_weighting_method_combo_box = WeightingMethodComboBox()
        self.observation_weighting_method_tuning_constants = QDoubleSpinBoxList(3)

        self.free_adjustment_weighting_method_label = QLabel(
            "Free adjustment weighting methods"
        )
        self.free_adjustment_checkbox = QCheckBox()
        self.free_adjustment_weighting_method_combo_box = WeightingMethodComboBox()
        self.free_adjustment_weighting_method_tuning_constants = QDoubleSpinBoxList(3)

        self.report_label = QLabel("Report:")
        self.report_checkbox = QCheckBox()
        self.report_line_edit = QLineEdit()
        self.report_button = QPushButton("...")

        self.output_label = QLabel("Select output path:")
        self.output_line_edit = QLineEdit()
        self.output_button = QPushButton("...")
        self.output_saving_mode_menu = SavingModeMenu()

        self.ok_button = QPushButton("OK")

        main_layout = self._build_main_layout()
        self.setLayout(main_layout)

    def _build_main_layout(self) -> QVBoxLayout:
        """Build and return the main vertical layout."""
        input_file_layouts = self._build_input_file_layouts()
        weighting_methods_layout = self._build_weighting_methods_layout()
        report_layout = self._build_report_layout()
        output_layout = self._build_output_layout()

        main_layout = QVBoxLayout()
        for input_file_layout in input_file_layouts:
            main_layout.addLayout(input_file_layout)
        main_layout.addLayout(weighting_methods_layout)
        main_layout.addLayout(report_layout)
        main_layout.addLayout(output_layout)
        main_layout.addWidget(self.ok_button)
        return main_layout

    # Input files layout ==================================================
    def _build_input_file_layouts(self) -> FileLayout:
        """Yield layouts for input file selection."""
        labels = (self.measurements_label, self.controls_label)
        line_edits = (self.measurements_line_edit, self.controls_line_edit)
        buttons = (self.measurements_button, self.controls_button)

        for label, line_edit, button in zip(labels, line_edits, buttons):
            yield FileLayout(label=label, line_edit=line_edit, button=button)

    # Weighting methods layout ==================================================
    def _build_weighting_methods_layout(self) -> QHBoxLayout:
        """Build and return the weighting methods layout."""
        self._configure_weighting_methods_widgets()

        observation_weighting_methods_layout = WeightingMethodLayout(
            label=self.observation_weighting_method_label,
            combo_box=self.observation_weighting_method_combo_box,
            tuning_constants=self.observation_weighting_method_tuning_constants,
        )
        free_adjustment_weighting_methods_layout = WeightingMethodLayout(
            label=self.free_adjustment_weighting_method_label,
            checkbox=self.free_adjustment_checkbox,
            combo_box=self.free_adjustment_weighting_method_combo_box,
            tuning_constants=self.free_adjustment_weighting_method_tuning_constants,
        )

        weighting_methods_row_layout = QHBoxLayout()
        weighting_methods_row_layout.addLayout(
            observation_weighting_methods_layout, stretch=1
        )
        weighting_methods_row_layout.addLayout(
            free_adjustment_weighting_methods_layout, stretch=1
        )

        return weighting_methods_row_layout

    def _configure_weighting_methods_widgets(self):
        """Configure widgets for weighting methods section."""
        self.free_adjustment_weighting_method_combo_box.setEnabled(False)
        for tuning_constants in (
            self.observation_weighting_method_tuning_constants,
            self.free_adjustment_weighting_method_tuning_constants,
        ):
            self._configure_tuning_constants(tuning_constants)

    def _configure_tuning_constants(self, tuning_constants: QDoubleSpinBoxList) -> None:
        """Configure properties for tuning constant spin boxes."""
        tuning_constants.setDecimals(3)
        tuning_constants.setRange(0.0, 100.0)
        tuning_constants.setSingleStep(0.01)
        tuning_constants.hide()

    # Report layout ===================================================
    def _build_report_layout(self) -> FileLayout:
        """Build and return the report file layout."""
        self._configure_report_layout_widgets()
        return FileLayout(
            label=self.report_label,
            checkbox=self.report_checkbox,
            line_edit=self.report_line_edit,
            button=self.report_button,
        )

    def _configure_report_layout_widgets(self) -> None:
        """Configure widgets for the report section."""
        self.report_line_edit.setEnabled(False)
        self.report_button.setEnabled(False)

    # Output layout ===================================================
    def _build_output_layout(self) -> FileLayout:
        """Build and return the output file layout."""
        self._configure_output_layout_widgets()
        return FileLayout(
            label=self.output_label,
            line_edit=self.output_line_edit,
            button=self.output_button,
        )

    def _configure_output_layout_widgets(self) -> None:
        """Configure widgets for the output section."""
        self.output_line_edit.setPlaceholderText("[Temporary layer]")
        self.output_button.setMenu(self.output_saving_mode_menu)
