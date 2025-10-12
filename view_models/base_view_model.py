# Coding: UTF-8

# Copyright (C) 2025 Michał Prędki
# Licensed under the GNU General Public License v3.0.
# Full text of the license can be found in the LICENSE file in the repository.

from qgis.PyQt.QtCore import QObject


class BaseViewModel(QObject):

    def __init__(self, model=None) -> None:
        super().__init__()

    def reset_state(self) -> None:
        """Reset the params state and emit signals."""
        raise NotImplementedError(
            f"{self.__class__.__name__} must implement bind_widgets()"
        )
