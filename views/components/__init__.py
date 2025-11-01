# Coding: UTF-8

# Copyright (C) 2025 Michał Prędki
# Licensed under the GNU General Public License v3.0.
# Full text of the license can be found in the LICENSE file in the repository.

"""
================================== Components Module ===================================

This module contains reusable user interface (UI) components for the QNET QGIS plugin.
It serves as a toolbox for specialized widgets, layouts, and utility functions that
are used across multiple views in the plugin to simplify widget creation and configuration.

Structure
---------
- widgets.py: Custom widgets used in the plugin
- layouts.py: Predefined layout classes for consistent widget arrangement
- utils.py: Utility functions for getting file path from dialog and widget state update

Inheritance Relations
---------------------
- Widget components inherit from standard Qt widgets
- QNet specific message box inherit from QNetMessageBox:

  QMessageBox
  └── QNetMessageBox
      ├── QNetErrorMessageBox
      ├── QNetInformationBox
      ├── QNetWarningBox
      └── QNetQuestionBox
  
- Layout classes inherit from Qt layout classes

========================================================================================
"""
