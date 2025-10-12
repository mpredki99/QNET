# Coding: UTF-8

# Copyright (C) 2025 Michał Prędki
# Licensed under the GNU General Public License v3.0.
# Full text of the license can be found in the LICENSE file in the repository.

from qgis.PyQt.QtWidgets import QLayout, QWidget


class BaseViewUI(QWidget):
    """This class provides a template for building layouts in UI dialogs."""

    def __init__(self):
        super().__init__()

    def setLayout(self, layout: QLayout) -> None:
        """Set the layout for the UI widget with zero margins."""
        layout.setContentsMargins(0, 0, 0, 0)
        super().setLayout(layout)

    def build_layout(self):
        """Build and return the main layout for the dialog."""
        raise NotImplementedError(
            f"{self.__class__.__name__} must implement build_layout()"
        )
