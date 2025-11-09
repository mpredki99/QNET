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
    ViewModel for managing weighting methods and tuning constants used in the adjustment.

    This class encapsulates logic related to weighting method configuration for both
    `observation adjustment` and `free adjustment`. It tracks the selected weighting
    methods and their associated tuning constants, updating them as needed. When a new
    weighting method is selected, the ViewModel automatically retrieves its default
    tuning constants from the `weighting_methods` module.

    Signals
    -------
    - observation_weighting_method_changed : pyqtSignal(str)
        Emitted when the observation weighting method changes.
    - observation_tuning_constants_changed : pyqtSignal(tuple)
        Emitted when any of the observation tuning constant values change.
    - free_adjustment_switched : pyqtSignal(bool)
        Emitted when free adjustment mode is toggled.
    - free_adjustment_weighting_method_changed : pyqtSignal(str)
        Emitted when the free adjustment weighting method changes.
    - free_adjustment_tuning_constants_changed : pyqtSignal(tuple)
        Emitted when any of the free adjustment tuning constant values change.

    Attributes
    ----------
    - params : AdjustmentParams
        Data transfer object containing current weighting and tuning configuration.
    """

    observation_weighting_method_changed = pyqtSignal(str)
    observation_tuning_constants_changed = pyqtSignal(tuple)

    free_adjustment_switched = pyqtSignal(bool)
    free_adjustment_weighting_method_changed = pyqtSignal(str)
    free_adjustment_tuning_constants_changed = pyqtSignal(tuple)

    def __init__(self) -> None:
        """Initialize the ViewModel with default adjustment parameters."""
        super().__init__()
        self.params = AdjustmentParams()

    def reset_state(self) -> None:
        """Reset all weighting method parameters to defaults and emit signals."""
        self.params = AdjustmentParams()
        self._emit_observation_weighting_method_changed()
        self._emit_observation_tuning_constants_changed()
        self._emit_free_adjustment_switched()
        self._emit_free_adjustment_weighting_method_changed()
        self._emit_free_adjustment_tuning_constants_changed()

    def update_observation_weighting_method(self, method_label: str) -> None:
        """Update the observation weighting method and emit change signals."""
        self._update_weighting_method(
            method_label,
            "observation_weighting_method",
            "observation_tuning_constants",
            self._emit_observation_weighting_method_changed,
            self._emit_observation_tuning_constants_changed,
        )

    def update_free_adjustment_weighting_method(self, method_label: str) -> None:
        """Update the free adjustment weighting method and emit change signals."""
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
        """Update observation tuning constants and emit change signals."""
        self._update_tuning_constants(
            "observation_tuning_constants",
            tuning_constant_values,
            self._emit_observation_tuning_constants_changed,
        )

    def update_free_adjustment_tuning_constants(
        self, tuning_constant_values: Tuple[float]
    ) -> None:
        """Update free adjustment tuning constants and emit change signals."""
        self._update_tuning_constants(
            "free_adjustment_tuning_constants",
            tuning_constant_values,
            self._emit_free_adjustment_tuning_constants_changed,
        )

    def switch_free_adjustment(self, state: int) -> None:
        """Toggle free adjustment mode and emit change signal."""
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
        """Update weighting method and its corresponding tuning constants."""
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
        """Update tuning constant values."""
        tuning_constants = getattr(self.params, tuning_constants_param)

        if tuning_constants is None:
            return

        for key, value in zip(tuning_constants.keys(), tuning_constants_values):
            tuning_constants[key] = value
        emit_tuning_constants_changed()

    def _emit_free_adjustment_switched(self) -> None:
        """Emit free adjustment switched signal."""
        self.free_adjustment_switched.emit(self.params.perform_free_adjustment)

    def _emit_observation_weighting_method_changed(self) -> None:
        """Emit observation weighting method changed signal."""
        self._emit_weighting_method_changed(
            self.observation_weighting_method_changed,
            self.params.observation_weighting_method,
        )

    def _emit_free_adjustment_weighting_method_changed(self) -> None:
        """Emit free adjustment weighting method changed signal."""
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
        """Emit free adjustment tuning constants changed signal."""
        self._emit_tuning_constants_changed(
            self.free_adjustment_tuning_constants_changed,
            self.params.free_adjustment_tuning_constants,
        )

    def _emit_observation_tuning_constants_changed(self) -> None:
        """Emit observation tuning constants changed signal."""
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
