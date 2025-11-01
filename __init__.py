# Coding: UTF-8

# Copyright (C) 2025 Michał Prędki
# Licensed under the GNU General Public License v3.0.
# Full text of the license can be found in the LICENSE file in the repository.

"""
=================================== QNET QGIS Plugin ===================================

QNET is a QGIS plugin for least squares adjustment of surveying control networks.

This module extends `sys.path` to include the bundled vendor libraries directory, 
ensuring all dependencies are accessible. The `classFactory` function serves as the 
QGIS plugin entry point, returning an instance of the main `QNet` class.

Structure
---------
- qnet.py: Main plugin class integrating with QGIS interface
- models/: Business logic and data processing
- view_models/: Presentation logic and state management
- views/: User interface components
- dto/: Data transfer objects
- utils/: Plugin-specific utilities
- icons/: Plugin icons
- lib/pysurv/: Core surveying computation library
- lib/pydantic/: Validation library used in pysurv internals

Architecture
------------
The plugin follows the MVVM (Model-View-ViewModel) architectural pattern, ensuring
clear separation of concerns and maintainability:

Model Layer (models/):
- `MainModel`: Central coordinator aggregating sub-models
- `PySurvModel`: Wraps the pysurv library for computational operations
- `QgisModel`: Handles QGIS-specific workflows
- results/: Result objects representing operation outcomes

ViewModel Layer (view_models/):
- `BaseViewModel`: Base class inheriting from QObject for Qt signal support
- `BaseViewModelSection`: Base class for section-specific ViewModels
- `MainViewModel`: Coordinates sub-ViewModels and main data-binding entry point
- Section ViewModels: `InputFilesViewModel`, `WeightingMethodsViewModel`, 
    `ReportViewModel`, `OutputViewModel`

View Layer (views/):
- `BaseViewUI` / `BaseViewSectionUI`: UI base classes for layout building
- `BaseView`: Generic base class for ViewModel binding
- `BaseViewSection`: Base class for section views
- `MainView`: Main dialog window coordinating all sections
- Section Views: `InputFilesView`, `WeightingMethodsView`, `OutputView`, `ReportView`
- components/: Reusable UI widgets, layouts, and utilities

=======================================================================================
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
