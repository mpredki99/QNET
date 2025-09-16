# Coding: UTF-8

# Copyright (C) 2025 Michał Prędki
# Licensed under the GNU General Public License v3.0.
# Full text of the license can be found in the LICENSE file in the repository.

from typing import Any, Tuple

from qgis.PyQt.QtWidgets import QAction, QComboBox, QDoubleSpinBox, QMenu

from ...infrastructure.weighting_methods import WEIGHTING_METHODS


class QDoubleSpinBoxList(list):
    """
    A list subclass containing QDoubleSpinBox widgets.
    Allows batch method calls and attribute access to all contained spin boxes.
    """

    def __init__(self, n: int) -> None:
        super().__init__(QDoubleSpinBox() for _ in range(n))

    def __getattr__(self, name: str) -> Any:
        """Delegate attribute access or method calls to all QDoubleSpinBox items."""
        if not self:
            raise AttributeError(f"{self.__class__.__name__} is empty")

        def wrapper(*args, **kwargs):
            return [getattr(spin_box, name)(*args, **kwargs) for spin_box in self]

        attr = getattr(QDoubleSpinBox, name)
        return wrapper if callable(attr) else attr


class WeightingMethodComboBox(QComboBox):
    """
    QComboBox widget for selecting a weighting method.
    Populates itself with available methods from WEIGHTING_METHODS.
    """

    def __init__(self, weighting_methods=None) -> None:
        super().__init__()
        self._populate(weighting_methods)

    def _populate(self, weighting_methods):
        """Populate widget with supported weighting methods."""
        weighting_methods = weighting_methods or [
            method for method in WEIGHTING_METHODS.keys()
        ]
        self.addItems(weighting_methods)


class SavingModeMenu(QMenu):
    """
    QMenu widget for selecting the saving mode.
    Adds actions for each available saving mode.
    """

    def __init__(self) -> None:
        super().__init__()
        for action in self._define_output_mode_actions():
            self.addAction(action)

    def _define_output_mode_actions(self) -> Tuple[QAction]:
        """Return a tuple of QAction objects for output modes."""
        return (QAction("Temporary layer", self), QAction("To file", self))
