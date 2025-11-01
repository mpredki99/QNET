# Coding: UTF-8

# Copyright (C) 2025 Michał Prędki
# Licensed under the GNU General Public License v3.0.
# Full text of the license can be found in the LICENSE file in the repository.

"""
-------------------------------- ViewModel Layer --------------------------------------

This package contains all ViewModel classes for the QNET QGIS plugin. ViewModels mediate 
between the core business logic (Models) and the user interface (Views), exposing plugin 
state through Qt signals.

Inheritance Structure:
----------------------
- `BaseViewModel`: Inherit from `QObject` to leverage Qt's signal/slot mechanism.  
- `BaseViewModelSection`: Abstract class that provide interface for implementation of sub-ViewModels.
- `MainViewModel`: coordinates sub-ViewModels and serves as the main entry point for data-binding.

---------------------------------------------------------------------------------------
"""
