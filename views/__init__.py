# Coding: UTF-8

# Copyright (C) 2025 Michał Prędki
# Licensed under the GNU General Public License v3.0.
# Full text of the license can be found in the LICENSE file in the repository.

"""
==================================== View Layer ========================================

This package contains all view components for the QNET QGIS plugin. These modules
are responsible for rendering the user interface, displaying data and connecting 
UI events and capturing user input to their corresponding ViewModels.

Structure
---------
- base_views_ui.py: Defines abstract base classes for building dialog layouts
- base_views.py: Defines generic base class for ViewModel binding functionality
- main_view_ui.py: Defines main dialog widget layout, arranges section views
- main_view.py: Combines UI layout with ViewModel binding, coordinates all section views

Section Views: 
- *_view_ui.py: Define widget arrangements and static UI elements
- *_view.py: Manage widgets and ViewModel signal connections

Inheritance Relations
--------------------
UI Hierarchy:

QDialog (Qt base class)
└── BaseViewUI (abstract)
    ├── BaseViewSectionUI (abstract)
    │   ├── InputFilesViewUI
    │   ├── WeightingMethodsViewUI
    │   ├── OutputViewUI
    │   └── ReportViewUI
    └── MainViewUI

ViewModel Binding Hierarchy:

BaseView[ViewModelType] (generic, abstract)
├── BaseViewSection[ViewModelType] (generic, abstract)
│   ├── InputFilesView
│   ├── WeightingMethodsView
│   ├── OutputView
│   └── ReportView
└── MainView

In the View layer, each View class uses multiple inheritance to combine its corresponding
UI layout class with the relevant generic BaseView class for ViewModel binding.

Submodules
----------
- components/: Collection of reusable UI components

========================================================================================
"""
