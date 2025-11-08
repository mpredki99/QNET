# Coding: UTF-8

# Copyright (C) 2025 Michał Prędki
# Licensed under the GNU General Public License v3.0.
# Full text of the license can be found in the LICENSE file in the repository.

from qgis.PyQt.QtWidgets import QCheckBox, QHBoxLayout, QLabel

from .base_views_ui import BaseViewSectionUI
from .components.layouts import WeightingMethodLayout
from .components.widgets import QDoubleSpinBoxList, WeightingMethodComboBox


class WeightingMethodsViewUI(BaseViewSectionUI):
    """
    UI base class for the Weighting Methods section in the QNET plugin.

    This class defines and arranges the widgets used for configuring observation and
    free adjustment weighting methods. It provides controls for method selection,
    optional free adjustment enablement, and tuning constant values configuration.

    Attributes
    ----------
    - TUNING_CONSTANTS_DECIMALS : int
        Number of decimal places displayed in the tuning constant spin boxes.
    - TUNING_CONSTANTS_RANGE : tuple[float, float]
        Minimum and maximum values allowed for tuning constants.
    - TUNING_CONSTANTS_STEP : float
        Step size used when adjusting tuning constant values.
    - observation_weighting_method_label : QLabel
        Label for the observation weighting method selection.
    - observation_weighting_method_combo_box : WeightingMethodComboBox
        Drop-down list for selecting the observation weighting method.
    - observation_weighting_method_tuning_constants : QDoubleSpinBoxList
        List of spin boxes for defining observation weighting method tuning constant values.
    - free_adjustment_weighting_method_label : QLabel
        Label for the free adjustment weighting method section.
    - free_adjustment_checkbox : QCheckBox
        Checkbox enabling or disabling the free adjustment option.
    - free_adjustment_weighting_method_combo_box : WeightingMethodComboBox
        Drop-down list for selecting the free adjustment weighting method.
    - free_adjustment_weighting_method_tuning_constants : QDoubleSpinBoxList
        List of spin boxes for defining free adjustment weighting method tuning constant values.
    """

    # Layout constants
    TUNING_CONSTANTS_DECIMALS = 3
    TUNING_CONSTANTS_RANGE = (0.0, 100.0)
    TUNING_CONSTANTS_STEP = 0.01

    def __init__(self) -> None:
        """Initialize all widgets used for the section View."""
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
        """Build and return the layout for the weighting methods section."""
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

        layout = QHBoxLayout()
        layout.addLayout(observation_weighting_methods_layout, stretch=1)
        layout.addLayout(free_adjustment_weighting_methods_layout, stretch=1)
        return layout

    def _configure_widgets(self) -> None:
        """Configure widgets for weighting methods section."""
        for tuning_constants in (
            self.observation_weighting_method_tuning_constants,
            self.free_adjustment_weighting_method_tuning_constants,
        ):
            self._configure_tuning_constants(tuning_constants)

    def _configure_tuning_constants(self, tuning_constants: QDoubleSpinBoxList) -> None:
        """Configure properties for tuning constant spin boxes."""
        tuning_constants.setDecimals(self.TUNING_CONSTANTS_DECIMALS)
        tuning_constants.setRange(*self.TUNING_CONSTANTS_RANGE)
        tuning_constants.setSingleStep(self.TUNING_CONSTANTS_STEP)
        tuning_constants.hide()
