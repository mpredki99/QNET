# Coding: UTF-8

# Copyright (C) 2025 Michał Prędki
# Licensed under the GNU General Public License v3.0.
# Full text of the license can be found in the LICENSE file in the repository.

"""
==================================== ViewModel Layer ===================================

This package contains all ViewModel classes for the QNET QGIS plugin. ViewModels
mediate between the core business logic (Models) and the user interface (Views),
following the MVVM architectural pattern. They expose plugin state through Qt
signals and handle user interactions by delegating to Models.

Structure
---------
- base_view_models.py: Define base classes for all ViewModels
- main_view_model.py: Main coordinator ViewModel, aggregates and coordinates sub-ViewModels

Section ViewModels:
- input_files_view_model.py: Manages input file selection
- weighting_methods_view_model.py: Manages weighting method and tuning constant values selection
- report_view_model.py: Handles report file path selection
- output_view_model.py: Handles export path selection and manages output configuration

- workflow.py: Manages the execution of model methods

Inheritance Relations
---------------------
QObject (Qt base class)
└── BaseViewModel
    ├── MainViewModel
    └── BaseViewModelSection (abstract)
        ├── InputFilesViewModel
        ├── WeightingMethodsViewModel
        ├── OutputViewModel
        └── ReportViewMode

========================================================================================
"""
