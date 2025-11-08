# Coding: UTF-8

# Copyright (C) 2025 Michał Prędki
# Licensed under the GNU General Public License v3.0.
# Full text of the license can be found in the LICENSE file in the repository.

from itertools import zip_longest
from typing import Optional, Tuple

from ..utils.weighting_methods import get_method_label_from_name
from ..view_models.weighting_methods_view_model import WeightingMethodsViewModel
from .base_views import BaseViewSection
from .components.utils import update_checkbox_state, update_combo_box_text
from .components.widgets import QDoubleSpinBoxList, WeightingMethodComboBox
from .weighting_methods_view_ui import WeightingMethodsViewUI


class WeightingMethodsView(
    WeightingMethodsViewUI, BaseViewSection[WeightingMethodsViewModel]
):
    """
    View class for the Weighting Methods section in the QNET plugin.

    This class connects the Weighting Methods UI with its corresponding 
    `WeightingMethodsViewModel`, enabling two-way data binding between user interactions
    and application state. It manages the selection of observation and free adjustment
    weighting methods, the activation of the free adjustment mode, and the configuration
    of their tuning constants.The class binds UI widget events to ViewModel handlers and 
    updates the interface in response to ViewModel signals.


    Attributes
    ----------
    - view_model : WeightingMethodsViewModel, optional
        Reference to the associated ViewModel controlling weighting methods logic.
    """

    def __init__(self, view_model: Optional[WeightingMethodsViewModel] = None) -> None:
        """
        Initialize the WeightingMethodsView.

        Parameters
        ----------
        - view_model : WeightingMethodsViewModel, optional
            Reference to the associated WeightingMethodsViewModel.
        """
        super().__init__()
        self.view_model = view_model

    def bind_widgets(self) -> None:
        """Bind UI widget signals to their ViewModel handlers."""
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
        """Bind ViewModel signals to UI update methods."""
        self.view_model.observation_weighting_method_changed.connect(
            self.update_observation_weighting_method_combo_box
        )
        self.view_model.observation_tuning_constants_changed.connect(
            self.update_observation_weighting_method_tuning_constants
        )
        self.view_model.free_adjustment_switched.connect(self.enable_free_adjustment)
        self.view_model.free_adjustment_weighting_method_changed.connect(
            self.update_free_adjustment_weighting_method_combo_box
        )
        self.view_model.free_adjustment_tuning_constants_changed.connect(
            self.update_free_adjustment_weighting_method_tuning_constants
        )

    def update_observation_weighting_method_combo_box(self, method_name: str) -> None:
        """Update observation weighting method combo box current text."""
        self._update_weighting_method_combo_box_text(
            self.observation_weighting_method_combo_box, method_name
        )

    def update_free_adjustment_weighting_method_combo_box(self, method_name: str) -> None:
        """Update free adjustment weighting method combo box current text."""
        self._update_weighting_method_combo_box_text(
            self.free_adjustment_weighting_method_combo_box, method_name
        )

    def enable_free_adjustment(self, enabled: bool) -> None:
        """Enable or disable free adjustment control widgets."""
        update_checkbox_state(self.free_adjustment_checkbox, 2 if enabled else 0)
        self.free_adjustment_weighting_method_combo_box.setEnabled(enabled)
        self.free_adjustment_weighting_method_tuning_constants.setEnabled(enabled)

    def update_observation_weighting_method_tuning_constants(
        self, tuning_constants_values: Tuple[float]
    ) -> None:
        """Update observation weighting method tuning constant values."""
        self._update_tuning_constant_spin_boxes(
            self.observation_weighting_method_tuning_constants,
            tuning_constants_values,
        )

    def update_free_adjustment_weighting_method_tuning_constants(
        self, tuning_constant_values: Tuple[float]
    ) -> None:
        """Refresh free adjustment weighting method tuning constants values."""
        self._update_tuning_constant_spin_boxes(
            self.free_adjustment_weighting_method_tuning_constants,
            tuning_constant_values,
        )

    def _update_weighting_method_combo_box_text(
        self, combo_box: WeightingMethodComboBox, method_name: str
    ) -> None:
        """Set combo box index based on method name."""
        method_label = get_method_label_from_name(method_name)
        update_combo_box_text(combo_box, method_label)

    def _update_tuning_constant_spin_boxes(
        self,
        tuning_constants_list: QDoubleSpinBoxList,
        tuning_constants_values: Tuple[float],
    ) -> None:
        """Update value and show/hide tuning constant spin boxes."""
        for spin_box, c in zip_longest(
            tuning_constants_list, tuning_constants_values, fillvalue=None
        ):
            if c is not None:
                spin_box.setValue(c)
                spin_box.show()
            else:
                spin_box.hide()
