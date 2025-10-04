# Coding: UTF-8

# Copyright (C) 2025 Michał Prędki
# Licensed under the GNU General Public License v3.0.
# Full text of the license can be found in the LICENSE file in the repository.

import os

from qgis.core import *
from qgis.gui import *
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction

from .view_models import MainViewModel
from .views import MainView


class QNet:
    def __init__(self, iface):
        self.iface = iface
        self.action = None

    def initGui(self):
        plugin_dir = os.path.dirname(__file__)
        icon_path = os.path.join(plugin_dir, "icons/icon.png")
        self.action = QAction(QIcon(icon_path), "QNET", self.iface.mainWindow())
        self.action.triggered.connect(self.run)
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu("&QNET", self.action)

    def unload(self):
        self.iface.removePluginMenu("&QNET", self.action)
        self.iface.removeToolBarIcon(self.action)

    def run(self):
        model = None
        view_model = MainViewModel(model)
        view = MainView(view_model)
        view.exec_()
