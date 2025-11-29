# Coding: UTF-8

# Copyright (C) 2025 Michał Prędki
# Licensed under the GNU General Public License v3.0.
# Full text of the license can be found in the LICENSE file in the repository.

"""
==================================== Tasks Submodule ===================================

This package provides the task execution infrastructure used by the QNET plugin to run 
model layer operations within QGIS.

Structure
---------
- task_step.py: Represents a single step to be executed by a QNetBackgroundTask
- qnet_background_task.py: Background task executor for running QNET model operations

Inheritance Relations
---------------------
QgsTask (QGIS abstract base class)
└── QNetBackgroundTask

========================================================================================
"""
