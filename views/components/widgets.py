# Coding: UTF-8

# Copyright (C) 2025 Michał Prędki
# Licensed under the GNU General Public License v3.0.
# Full text of the license can be found in the LICENSE file in the repository.

from typing import Any, Optional, Tuple

from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QDoubleSpinBox
from qgis.PyQt.QtCore import QObject, pyqtSignal
from qgis.PyQt.QtWidgets import QAction, QComboBox, QDoubleSpinBox, QMenu

from ...infrastructure.weighting_methods import WEIGHTING_METHODS


class QDoubleSpinBoxList(QObject):
    """
    A widget containing QDoubleSpinBox widgets as a list.
    Allows batch method calls and attribute access to all contained spin boxes.
    """

    listValueChanged = pyqtSignal(tuple)

    def __init__(self, n: int, parent: Optional[Any] = None) -> None:
        super().__init__(parent)
        self._items = [QDoubleSpinBox() for _ in range(n)]
        self.bind_spin_boxes()

    def __getattr__(self, name: str) -> Any:
        """Delegate attribute access or method calls to list container or QDoubleSpinBox items."""
        if hasattr(list, name):
            return self._handle_list_method(name)
        if hasattr(QDoubleSpinBox, name):
            return self._handle_spin_box_method(name)
        raise AttributeError(f"{self.__class__.__name__} has no attribute {name}")

    def __len__(self) -> int:
        """Return the number of spin boxes contained."""
        return len(self._items)

    def __iter__(self):
        """Return iterator over spin boxes."""
        return iter(self._items)

    def __getitem__(self, index: int) -> QDoubleSpinBox:
        """Get spin box at index."""
        return self._items[index]

    def __setitem__(self, index: int, value: QDoubleSpinBox) -> None:
        """Set spin box at index."""
        if not isinstance(value, QDoubleSpinBox):
            raise TypeError(
                f"{self.__class__.__name__} can constains only QDoubleSpinBox objects"
            )
        self._items[index] = value

    def bind_spin_boxes(self) -> None:
        """Bind valueChanged signal of each spin box to emit_list_value_changed."""
        for sb in self._items:
            sb.valueChanged.connect(self.emit_list_value_changed)

    def emit_list_value_changed(self, _: float) -> None:
        """Emit listValueChanged signal with current visible spin box values."""
        values = tuple(
            spin_box.value() for spin_box in self._items if spin_box.isVisible()
        )
        self.listValueChanged.emit(values)

    def _handle_list_method(self, name: str) -> Any:
        """Handle list method delegation."""

        def wrapper(*args, **kwargs):
            return getattr(self._items, name)(*args, **kwargs)

        attr = getattr(list, name)
        return wrapper if callable(attr) else attr

    def _handle_spin_box_method(self, name: str) -> Any:
        """Handle QDoubleSpinBox method delegation."""

        def wrapper(*args, **kwargs):
            return [getattr(sb, name)(*args, **kwargs) for sb in self._items]

        attr = getattr(QDoubleSpinBox, name)
        return wrapper if callable(attr) else attr


class WeightingMethodComboBox(QComboBox):
    """
    QComboBox widget for selecting a weighting method.
    Populates itself with available methods from WEIGHTING_METHODS.
    """

    def __init__(self, weighting_methods: Optional[list] = None) -> None:
        super().__init__()
        self._populate(
            weighting_methods or [method for method in WEIGHTING_METHODS.keys()]
        )

    def _populate(self, weighting_methods: list) -> None:
        """Populate widget with supported weighting methods."""
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
