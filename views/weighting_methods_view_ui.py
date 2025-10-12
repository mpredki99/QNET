# Coding: UTF-8

# Copyright (C) 2025 Michał Prędki
# Licensed under the GNU General Public License v3.0.
# Full text of the license can be found in the LICENSE file in the repository.

from qgis.PyQt.QtWidgets import QCheckBox, QHBoxLayout, QLabel

from .base_view_ui import BaseViewUI
from .components.layouts import WeightingMethodLayout
from .components.widgets import QDoubleSpinBoxList, WeightingMethodComboBox


class WeightingMethodsViewUI(BaseViewUI):
    """
    UI base for the weighting methods section in the QNET plugin.

    Assembles and configures widgets for selecting observation and free adjustment
    weighting methods, including their tuning constants and enabling/disabling
    free adjustment options.
    """

    # Layout constants
    tuning_constants_decimals = 3
    tuning_constants_range = (0.0, 100.0)
    tuning_constants_step = 0.01

    def __init__(self) -> None:
        super().__init__()
        self.observation_weighting_method_label = QLabel(
            "Observations weighting methods:"
        )
        self.observation_weighting_method_combo_box = WeightingMethodComboBox()
        self.observation_weighting_method_tuning_constants = QDoubleSpinBoxList(3)

        self.free_adjustment_weighting_method_label = QLabel(
            "Free adjustment weighting methods:"
        )
        self.free_adjustment_checkbox = QCheckBox()
        self.free_adjustment_weighting_method_combo_box = WeightingMethodComboBox()
        self.free_adjustment_weighting_method_tuning_constants = QDoubleSpinBoxList(3)

        self._configure_widgets()
        layout = self.build_layout()
        self.setLayout(layout)

    def build_layout(self) -> QHBoxLayout:
        """Build and return the weighting methods layout."""
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

        main_layout = QHBoxLayout()
        main_layout.addLayout(observation_weighting_methods_layout, stretch=1)
        main_layout.addLayout(free_adjustment_weighting_methods_layout, stretch=1)
        return main_layout

    def _configure_widgets(self) -> None:
        """Configure widgets for weighting methods section."""
        for tuning_constants in (
            self.observation_weighting_method_tuning_constants,
            self.free_adjustment_weighting_method_tuning_constants,
        ):
            self._configure_tuning_constants(tuning_constants)

    def _configure_tuning_constants(self, tuning_constants: QDoubleSpinBoxList) -> None:
        """Configure properties for tuning constant spin boxes."""
        tuning_constants.setDecimals(self.tuning_constants_decimals)
        tuning_constants.setRange(*self.tuning_constants_range)
        tuning_constants.setSingleStep(self.tuning_constants_step)
        tuning_constants.hide()
