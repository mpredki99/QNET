# Coding: UTF-8

# Copyright (C) 2025 Michał Prędki
# Licensed under the GNU General Public License v3.0.
# Full text of the license can be found in the LICENSE file in the repository.

from qgis.PyQt.QtWidgets import QDialog, QLayout


class BaseViewUI(QDialog):
    """
    Provides a base template for building UI dialog layouts in the QNET plugin.

    This abstract class defines the structure for all dialog-based user interfaces
    in the View layer. Subclasses are required to implement the `build_layout()`
    method, which should create and return the main `QLayout` instance representing
    the structure of the dialog.
    """

    def __init__(self):
        """Initialize the base view UI and calls the constructor of the parent class."""
        super().__init__()

    def build_layout(self) -> QLayout:
        """Build and return the main layout of the dialog."""
        raise NotImplementedError(
            f"{self.__class__.__name__} must implement build_layout()"
        )


class BaseViewSectionUI(BaseViewUI):
    """
    Provides a base template for section-level UI layouts within the QNET plugin.

    This class extends `BaseViewUI` for building individual sections of the main dialog
    window. It standardizes layout handling by ensuring that all section widgets are
    initialized with zero layout margins for consistent visual alignment.
    """

    def setLayout(self, layout: QLayout) -> None:
        """Set the layout of the UI with zero margins."""
        layout.setContentsMargins(0, 0, 0, 0)
        super().setLayout(layout)
