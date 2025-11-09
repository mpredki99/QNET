# Coding: UTF-8

# Copyright (C) 2025 Michał Prędki
# Licensed under the GNU General Public License v3.0.
# Full text of the license can be found in the LICENSE file in the repository.

from qgis.PyQt.QtCore import QObject


class BaseViewModel(QObject):
    """
    Base class for all QNET ViewModels.

    Provides the foundational structure for the ViewModel layer, allowing all derived
    ViewModels to emit Qt signals for communication with their associated Views.
    """

    def __init__(self) -> None:
        """Initialize the BaseViewModel."""
        super().__init__()


class BaseViewModelSection(BaseViewModel):
    """
    Abstract base class for section-level ViewModels in the QNET plugin.

    Extends `BaseViewModel` to define a common interface and behavior for all
    section-specific ViewModels. Subclasses must implement the `reset_state()`
    method, which resets internal parameters and emits necessary update signals
    to restore default UI values.
    """

    def __init__(self) -> None:
        """Initialize the BaseViewModelSection."""
        super().__init__()

    def reset_state(self) -> None:
        """Reset the params state and emit signals."""
        raise NotImplementedError(
            f"{self.__class__.__name__} must implement reset_state()"
        )
