# Coding: UTF-8

# Copyright (C) 2025 Michał Prędki
# Licensed under the GNU General Public License v3.0.
# Full text of the license can be found in the LICENSE file in the repository.

"""
------------------------------------- Model layer -------------------------------------

This module contains logic models for the QNET QGIS plugin, organizing the business logic 
and core computational operations that support the ViewModel and View layers. The Model 
layer is structured into two submodels, each responsible for a specific aspect of the 
plugin's internal state and processing pipeline.

Structure:
----------
- `MainModel`: The central gateway for all model operations, aggregating the sub-models.
- `PySurvModel`: Wraps the logic of the pysurv package, covering all data import, 
  computation, and report-generation.
- `QgisModel`: Contains logic for QGIS-specific workflows, such as exporting adjusted 
  geometries to layers or files.

Submodules:
-----------
- `results`: Defines Result objects which are returned by model methods to represent the 
  outcome of computations and operations.

---------------------------------------------------------------------------------------
"""
