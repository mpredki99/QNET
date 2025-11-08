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
    Integrates the QNET plugin with the QGIS user interface.

    The class handles the initialization, activation, and cleanup processes required by
    the QGIS plugin API. It ensures that the plugin is properly connected and
    disconnected from the QGIS environment by implementing the required QGIS hooks
    (`initGui`, `unload`, `run`).

    Creates a QGIS `QAction` representing the plugin entry point. This action is added
    to the QGIS toolbar and Plugins.

    Attributes
    ----------
    - iface : Optional[qgis.utils.interfaces.QgisInterface]
        Reference to the QGIS interface object, providing access to the main QGIS
        window, menus, and toolbar for plugin integration.
    - action : Optional[QAction]
        The plugin's QAction instance added to the QGIS interface; connected to
        the plugin's `run()` method to open the main dialog.
    """

    def __init__(self, iface: Optional["QgisInterface"] = None) -> None:
        """
        Initialize a new QNET plugin instance.

        Parameters
        ----------
        - iface: QgisInterface, optional
            Reference to the active QGIS application interface. This object enabling
            the integration of the plugin's GUI components within the QGIS environment.
            * Notes: The `iface` parameter is automatically provided by the QGIS plugin
              manager during plugin loading. It should not be instantiated manually.
        """

        self.iface = iface
        self.action = None

    def initGui(self) -> None:
        """Register plugin action and adds it to the QGIS toolbars."""
        self.action = QAction(main_icon, "QNET", self.iface.mainWindow())
        self.action.triggered.connect(self.run)
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu("&QNET", self.action)

    def unload(self) -> None:
        """Unload the plugin action and removes it from QGIS toolbars."""
        self.iface.removePluginMenu("&QNET", self.action)
        self.iface.removeToolBarIcon(self.action)

    def run(self) -> None:
        """Instantiates core components and run the main dialog of the plugin."""
        model = MainModel()
        view_model = MainViewModel(model)
        view = MainView(view_model)
        view.exec()
