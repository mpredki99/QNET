# Coding: UTF-8
# Copyright (C) 2025 Michał Prędki
# Licensed under the GNU General Public License v3.0.

from typing import Callable, Dict, Optional, Tuple

from qgis.PyQt.QtCore import pyqtSignal

from ..dto.data_transfer_objects import AdjustmentParams
from ..utils.weighting_methods import get_method_name_and_tuning_constants
from .base_view_models import BaseViewModelSection


class WeightingMethodsViewModel(BaseViewModelSection):
    """
    ViewModel for managing weighting methods and tuning constants for both
    observation and free adjustment phases in the adjustment process.

    This class provides Qt signals to notify the UI of changes and methods
    to update the underlying adjustment parameters accordingly.
    """

    observation_weighting_method_changed = pyqtSignal(str)
    observation_tuning_constants_changed = pyqtSignal(tuple)

    free_adjustment_switched = pyqtSignal(bool)
    free_adjustment_weighting_method_changed = pyqtSignal(str)
    free_adjustment_tuning_constants_changed = pyqtSignal(tuple)

    def __init__(self) -> None:
        super().__init__()
        self.params = AdjustmentParams()

    def reset_state(self) -> None:
        """Reset the adjustment parameters and emit signals."""
        self.params = AdjustmentParams()
        self._emit_observation_weighting_method_changed()
        self._emit_observation_tuning_constants_changed()
        self._emit_free_adjustment_switched()
        self._emit_free_adjustment_weighting_method_changed()
        self._emit_free_adjustment_tuning_constants_changed()

    def update_observation_weighting_method(self, method_label: str) -> None:
        """Update the observation weighting method in adjustment params."""
        self._update_weighting_method(
            method_label,
            "observation_weighting_method",
            "observation_tuning_constants",
            self._emit_observation_weighting_method_changed,
            self._emit_observation_tuning_constants_changed,
        )

    def update_free_adjustment_weighting_method(self, method_label: str) -> None:
        """Update the free adjustment weighting method in adjustment params."""
        self._update_weighting_method(
            method_label,
            "free_adjustment_weighting_method",
            "free_adjustment_tuning_constants",
            self._emit_free_adjustment_weighting_method_changed,
            self._emit_free_adjustment_tuning_constants_changed,
        )

    def update_observation_tuning_constants(
        self, tuning_constant_values: Tuple[float]
    ) -> None:
        """Update the observation tuning constants in adjustment params."""
        self._update_tuning_constants(
            "observation_tuning_constants",
            tuning_constant_values,
            self._emit_observation_tuning_constants_changed,
        )

    def update_free_adjustment_tuning_constants(
        self, tuning_constant_values: Tuple[float]
    ) -> None:
        """Update the free adjustment tuning constants in adjustment params."""
        self._update_tuning_constants(
            "free_adjustment_tuning_constants",
            tuning_constant_values,
            self._emit_free_adjustment_tuning_constants_changed,
        )

    def switch_free_adjustment(self, state: int) -> None:
        """Switch the free adjustment state in adjustment params."""
        self.params.perform_free_adjustment = state == 2
        self._emit_free_adjustment_switched()

    def _update_weighting_method(
        self,
        method_label: str,
        weighting_method_param: str,
        tuning_constants_param: str,
        emit_method_changed: Callable[[], None],
        emit_tuning_constants_changed: Callable[[], None],
    ) -> None:
        """Update the weighting method and its tuning constants."""
        method_name, tuning_constants = get_method_name_and_tuning_constants(
            method_label
        )

        setattr(self.params, weighting_method_param, method_name)
        emit_method_changed()

        setattr(self.params, tuning_constants_param, tuning_constants or None)
        emit_tuning_constants_changed()

    def _update_tuning_constants(
        self,
        tuning_constants_param: str,
        tuning_constants_values: Tuple[float],
        emit_tuning_constants_changed: Callable[[], None],
    ) -> None:
        """Update the values of tuning constants."""
        tuning_constants = getattr(self.params, tuning_constants_param)

        if tuning_constants is None:
            return

        for key, value in zip(tuning_constants.keys(), tuning_constants_values):
            tuning_constants[key] = value
        emit_tuning_constants_changed()

    def _emit_free_adjustment_switched(self) -> None:
        """Emit free_adjustment_switched signal."""
        self.free_adjustment_switched.emit(self.params.perform_free_adjustment)

    def _emit_observation_weighting_method_changed(self) -> None:
        """Emit observation_weighting_method_changed signal."""
        self._emit_weighting_method_changed(
            self.observation_weighting_method_changed,
            self.params.observation_weighting_method,
        )

    def _emit_free_adjustment_weighting_method_changed(self) -> None:
        """Emit free_adjustment_weighting_method_changed signal."""
        self._emit_weighting_method_changed(
            self.free_adjustment_weighting_method_changed,
            self.params.free_adjustment_weighting_method,
        )

    def _emit_weighting_method_changed(
        self, signal: Callable[[str], None], method_name: str
    ) -> None:
        """Emit weighting method changed signal."""
        signal.emit(method_name)

    def _emit_free_adjustment_tuning_constants_changed(self) -> None:
        """Emit free_adjustment_tuning_constants_changed signal."""
        self._emit_tuning_constants_changed(
            self.free_adjustment_tuning_constants_changed,
            self.params.free_adjustment_tuning_constants,
        )

    def _emit_observation_tuning_constants_changed(self) -> None:
        """Emit observation_tuning_constants_changed signal."""
        self._emit_tuning_constants_changed(
            self.observation_tuning_constants_changed,
            self.params.observation_tuning_constants,
        )

    def _emit_tuning_constants_changed(
        self,
        signal: Callable[[Tuple[float, ...]], None],
        tuning_constants: Optional[Dict[str, float]],
    ) -> None:
        """Emit tuning constants changed signal."""
        signal.emit(
            tuple(tuning_constants.values())
            if tuning_constants is not None
            else tuple()
        )
