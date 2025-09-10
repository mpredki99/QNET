import os

from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction
from qgis.core import *
from qgis.gui import *

from .views import WindowDialog

class QNet:
    def __init__(self, iface):
        self.iface = iface
        self.action = None

    def initGui(self):
        plugin_dir = os.path.dirname(__file__)
        icon_path = os.path.join(plugin_dir, "icons/icon.png")
        self.action = QAction(QIcon(icon_path), "Plugin Test", self.iface.mainWindow())
        self.action.triggered.connect(self.run)
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu("&QNET", self.action)

    def unload(self):
        self.iface.removePluginMenu("&QNET", self.action)
        self.iface.removeToolBarIcon(self.action)

    def run(self):
        dialog = WindowDialog()
        dialog.exec_()
