# Coding: UTF-8

# Copyright (C) 2025 Michał Prędki
# Licensed under the GNU General Public License v3.0.
# Full text of the license can be found in the LICENSE file in the repository.

"""
=================================== Model Layer ========================================

This package contains the Model layer for the QNET QGIS plugin, implementing the
business logic and core computational operations.

This module contains logic models for the QNET QGIS plugin, organizing the business logic 
and core computational operations that support the ViewModel and View layers. The Model 
layer is structured into two submodels, each responsible for a specific aspect of the 
plugin's processing pipeline.

Structure
---------
- main_model.py: Central gateway, aggregates and coordinates sub-models
- pysurv_model.py: Wraps the pysurv library functionality (import data, least squares adjustment, generate report)
- qgis_model.py: Contains QGIS-specific workflow logic, exports adjusted coordinates to QGIS layers

Inheritance Relations
---------------------
All model classes are standalone dataclasses with no inheritance hierarchy.
They follow a composition pattern where `MainModel` aggregates `PySurvModel`
and `QgisModel` as component objects.

Submodules
----------
- results/: Defines Result objects returned by model methods

========================================================================================
"""
