# Coding: UTF-8

# Copyright (C) 2025 Michał Prędki
# Licensed under the GNU General Public License v3.0.
# Full text of the license can be found in the LICENSE file in the repository.

"""
------------------------------- View Layer --------------------------------------------

This package contains all view components for the QNET QGIS plugin. These modules are 
responsible for rendering the user interface and connecting UI events to their 
corresponding view models.

Inheritance Structure:
----------------------:
- `BaseViewUI` and `BaseViewSectionUI`: Abstract classes that provide foundational UI building logic.
- `BaseView` and `BaseViewSection`: Classes that encapsulate shared logic for ViewModel binding.
- UI classes: Define widget arrangements and static UI elements.
- View classes: Inherit from their respective `*UI` base classes and manage widget and ViewModel 
  signal connections.

Submodules:
-----------
- `components`: Collection of reusable UI components, widgets, layouts and utility functions.

---------------------------------------------------------------------------------------
"""
