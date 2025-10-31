# Coding: UTF-8

# Copyright (C) 2025 Michał Prędki
# Licensed under the GNU General Public License v3.0.
# Full text of the license can be found in the LICENSE file in the repository.

import sys
from pathlib import Path

plugin_dir = Path(__file__).parent
lib_dir = str(plugin_dir.joinpath("lib"))

if lib_dir not in sys.path:
    sys.path.insert(0, lib_dir)


def classFactory(iface) -> "QNet":
    """QGIS plugin entry point."""
    from .qnet import QNet

    return QNet(iface)
