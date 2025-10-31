# Coding: UTF-8

# Copyright (C) 2025 Michał Prędki
# Licensed under the GNU General Public License v3.0.
# Full text of the license can be found in the LICENSE file in the repository.

from itertools import zip_longest
from typing import Optional, Tuple

from ..infrastructure import get_method_label_from_name
from ..view_models.weighting_methods_view_model import WeightingMethodsViewModel
from .base_views import BaseViewSection
from .components.utils import update_checkbox_state, update_combo_box_text
from .components.widgets import QDoubleSpinBoxList, WeightingMethodComboBox
from .weighting_methods_view_ui import WeightingMethodsViewUI


class WeightingMethodsView(
    WeightingMethodsViewUI, BaseViewSection[WeightingMethodsViewModel]
):
    """
    View class for the weighting methods section in the QNET plugin.

    This class binds the UI widgets for selecting observation and free adjustment
    weighting methods, manages their tuning constants, and connects user interactions
    to the corresponding view model handlers. It also updates the UI in response to
    changes in the view model, such as enabling/disabling free adjustment options
    and refreshing tuning constant values.
    """

    def __init__(self, view_model: Optional[WeightingMethodsViewModel] = None) -> None:
        super().__init__()
        self.view_model = view_model

    def bind_widgets(self) -> None:
        """Bind UI widgets to their handlers."""
        self.observation_weighting_method_combo_box.currentTextChanged.connect(
            self.view_model.update_observation_weighting_method
        )
        self.observation_weighting_method_tuning_constants.listValueChanged.connect(
            self.view_model.update_observation_tuning_constants
        )
        self.free_adjustment_checkbox.stateChanged.connect(
            self.view_model.switch_free_adjustment
        )
        self.free_adjustment_weighting_method_combo_box.currentTextChanged.connect(
            self.view_model.update_free_adjustment_weighting_method
        )
        self.free_adjustment_weighting_method_tuning_constants.listValueChanged.connect(
            self.view_model.update_free_adjustment_tuning_constants
        )

    def bind_view_model_signals(self) -> None:
        """Bind view model signals to UI update methods."""
        self.view_model.observation_weighting_method_changed.connect(
            self.set_observation_weighting_method_combo_box
        )
        self.view_model.observation_tuning_constants_changed.connect(
            self.refresh_observation_weighting_method_tuning_constants
        )
        self.view_model.free_adjustment_switched.connect(self.enable_free_adjustment)
        self.view_model.free_adjustment_weighting_method_changed.connect(
            self.set_free_adjustment_weighting_method_combo_box
        )
        self.view_model.free_adjustment_tuning_constants_changed.connect(
            self.refresh_free_adjustment_weighting_method_tuning_constants
        )

    def set_observation_weighting_method_combo_box(self, method_name: str) -> None:
        """Set the current observation weighting method combo box index."""
        self._set_weighting_method_combo_box_index(
            self.observation_weighting_method_combo_box, method_name
        )

    def set_free_adjustment_weighting_method_combo_box(self, method_name: str) -> None:
        """Set the current free adjustment weighting method combo box index."""
        self._set_weighting_method_combo_box_index(
            self.free_adjustment_weighting_method_combo_box, method_name
        )

    def enable_free_adjustment(self, enabled: bool) -> None:
        """Enable or disable free adjustment control widgets."""
        update_checkbox_state(self.free_adjustment_checkbox, 2 if enabled else 0)
        self.free_adjustment_weighting_method_combo_box.setEnabled(enabled)
        self.free_adjustment_weighting_method_tuning_constants.setEnabled(enabled)

    def refresh_observation_weighting_method_tuning_constants(
        self, tuning_constants_values: Tuple[float]
    ) -> None:
        """Refresh observation weighting method tuning constants."""
        self._refresh_tuning_constant_spin_boxes(
            self.observation_weighting_method_tuning_constants,
            tuning_constants_values,
        )

    def refresh_free_adjustment_weighting_method_tuning_constants(
        self, tuning_constant_values: Tuple[float]
    ) -> None:
        """Refresh free adjustment weighting method tuning constants."""
        self._refresh_tuning_constant_spin_boxes(
            self.free_adjustment_weighting_method_tuning_constants,
            tuning_constant_values,
        )

    def _set_weighting_method_combo_box_index(
        self, combo_box: WeightingMethodComboBox, method_name: str
    ) -> None:
        """Set the combo box index to the given weighting method."""
        method_label = get_method_label_from_name(method_name)
        update_combo_box_text(combo_box, method_label)

    def _refresh_tuning_constant_spin_boxes(
        self,
        tuning_constants_list: QDoubleSpinBoxList,
        tuning_constants_values: Tuple[float],
    ) -> None:
        """Update and show/hide tuning constant spin boxes."""
        for spin_box, c in zip_longest(
            tuning_constants_list, tuning_constants_values, fillvalue=None
        ):
            if c is not None:
                spin_box.setValue(c)
                spin_box.show()
            else:
                spin_box.hide()
