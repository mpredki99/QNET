# Coding: UTF-8

# Copyright (C) 2025 Michał Prędki
# Licensed under the GNU General Public License v3.0.
# Full text of the license can be found in the LICENSE file in the repository.

"""
========================================================================================
Weighting Methods Utilities
========================================================================================

Module for managing robust weighting methods used in least squares adjustment 
computations within the QNET plugin.

Serves as an interface between human-readable method labels (as displayed
in the UI) and their corresponding internal identifiers and implementations from the
`pysurv.adjustment.robust` module.

It allows dynamic extraction of method-specific tuning constants, enabling automatic 
UI population for different robust weighting methods.

Usage Context
-------------
These utilities are primarily used by:
- The `WeightingMethodsViewModel` retreiving default tuning constant values
- The `WeightingMethodComboBox` widget (widgets.py) for retreiving the method labels.

Dependencies
------------
Relies on the `pysurv.adjustment.robust` module for robust weighting functions and their
parameter signatures.

========================================================================================
"""

from inspect import signature, unwrap
from typing import Dict, Tuple

from pysurv.adjustment import robust

WEIGHTING_METHODS = {
    "Ordinary": "ordinary",
    "Weighted": "weighted",
    "Huber": "huber",
    "Slope": "slope",
    "Hampel": "hampel",
    "Danish": "danish",
    "Epanechnikov": "epanechnikov",
    "Tukey": "tukey",
    "Jacobi": "jacobi",
    "Exponential": "exponential",
    "Choice Rule of Alternative": "cra",
    "Error Function": "error_func",
    "Cauchy": "cauchy",
    "T distribution": "t",
    "Bell Curve": "chain_bell",
    "Chain Curve": "chain",
    "Andrews": "andrews",
    "Wave": "wave",
    "Half-wave": "half_wave",
    "Wigner": "wigner",
    "Ellipse Curve": "ellipse_curve",
    "Trim": "trim",
}


def get_method_label_from_name(method_name: str) -> str:
    """Return the UI method label for a given PySurv weighting method name."""
    for label, name in WEIGHTING_METHODS.items():
        if name == method_name:
            return label
    return ""


def get_method_name_and_tuning_constants(
    method_label: str,
) -> Tuple[str, Dict[str, float]]:
    """Return the weighting method name and its tuning constants for a given label."""
    method_name = WEIGHTING_METHODS.get(method_label)
    func = getattr(robust, method_name, None)

    if not func:
        return method_name, dict()

    wrapped_func = unwrap(func)
    sig = signature(wrapped_func)

    return method_name, {
        key: value.default
        for key, value in sig.parameters.items()
        if isinstance(value.default, (int, float))
    }
