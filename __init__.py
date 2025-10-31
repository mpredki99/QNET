# Coding: UTF-8

# Copyright (C) 2025 Michał Prędki
# Licensed under the GNU General Public License v3.0.
# Full text of the license can be found in the LICENSE file in the repository.

"""
----------------------------------- QNET QGIS Plugin ----------------------------------

The QNET plugin embraces a clear modular structure driven by the MVVM (Model-View-ViewModel)
architecture, separating core logic, UI presentation, and data management for 
maintainability and testability. Key plugin features include:

- Importing survey input files;
- Configuring weighting methods and their tuning constants;
- Generating adjustment reports;
- Exporting the results as QGIS layer;
- Providing a user interface for surveying workflows.

All UI bindings, ViewModels, and main plugin logic are organized in submodules, with 
this initialization script responsible for bridging QGIS and the internal plugin logic.

---------------------------------------------------------------------------------------
"""


import sys
from pathlib import Path

"""Extend sys.path with bundled vendor libraries."""
plugin_dir = Path(__file__).parent
lib_dir = str(plugin_dir.joinpath("lib"))

if lib_dir not in sys.path:
    sys.path.insert(0, lib_dir)


def classFactory(iface) -> "QNet":
    """QGIS plugin entry point."""
    from .qnet import QNet

    return QNet(iface)
