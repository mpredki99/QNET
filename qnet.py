# Coding: UTF-8

# Copyright (C) 2025 Michał Prędki
# Licensed under the GNU General Public License v3.0.
# Full text of the license can be found in the LICENSE file in the repository.

from typing import Optional

from qgis.core import *
from qgis.gui import *
from qgis.PyQt.QtWidgets import QAction

from .icons.icons import main_icon
from .models.main_model import MainModel
from .view_models.main_view_model import MainViewModel
from .views.main_view import MainView


class QNet:
    """
    Main class for QNET QGIS plugin.

    Handles integration with the QGIS interface, including adding and removing
    plugin actions to the toolbar and initializing main dialog logic.
    Orchestrates plugin lifecycle methods required by the QGIS plugin infrastructure.
    """

    def __init__(self, iface: Optional["QgisInterface"]) -> None:
        self.iface = iface
        self.action = None

    def initGui(self) -> None:
        """Initialize the GUI for the plugin."""
        self.action = QAction(main_icon, "QNET", self.iface.mainWindow())
        self.action.triggered.connect(self.run)
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu("&QNET", self.action)

    def unload(self) -> None:
        """Unload the plugin and remove GUI elements."""
        self.iface.removePluginMenu("&QNET", self.action)
        self.iface.removeToolBarIcon(self.action)

    def run(self) -> None:
        """Run the main dialog of the plugin."""
        model = MainModel()
        view_model = MainViewModel(model)
        view = MainView(view_model)
        view.exec()
