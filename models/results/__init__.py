# Coding: UTF-8

# Copyright (C) 2025 Michał Prędki
# Licensed under the GNU General Public License v3.0.
# Full text of the license can be found in the LICENSE file in the repository.

"""
=================================== Results Module =====================================

This module defines Result objects used within the QNET plugin's Model layer to
represent the outcome of model operations. Result objects provide a standardized
way to communicate operation status, messages, and optional return data between
Models, ViewModels, and Views.

Dataflow
--------
1. Models perform computations and return `Result` objects
2. `Result` objects contain status, messages, and optional output data
3. ViewModels emit Qt signals based on `Result` status
4. Views update UI based on ViewModel signals

Structure
---------
- result.py: Defines `ResultStatus` and base class for all `Result` objects

Specialized result modules:
- import_result.py: Results from data import operation
- adjustment_result.py: Results from adjustment computations
- report_result.py: Results from report generation
- output_result.py: Results from export operation

Inheritance Relations
--------------------
Result (base class)
├── ImportResult
├── AdjustmentResult
├── OutputResult
└── ReportResult

========================================================================================
"""
