# Coding: UTF-8

# Copyright (C) 2025 Michał Prędki
# Licensed under the GNU General Public License v3.0.
# Full text of the license can be found in the LICENSE file in the repository.

import os
import sys

plugin_dir = os.path.dirname(__file__)
lib_dir = os.path.join(plugin_dir, "lib")
if lib_dir not in sys.path:
    sys.path.insert(0, lib_dir)


def classFactory(iface):
    from .qnet import QNet

    return QNet(iface)
