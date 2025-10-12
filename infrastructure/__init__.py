# Coding: UTF-8

# Copyright (C) 2025 Michał Prędki
# Licensed under the GNU General Public License v3.0.
# Full text of the license can be found in the LICENSE file in the repository.

from .weighting_methods import (
    WEIGHTING_METHODS,
    get_method_label_from_name,
    get_method_name_and_tuning_constants,
)

__all__ = [
    "get_method_name_and_tuning_constants",
    "get_method_label_from_name",
    "WEIGHTING_METHODS",
]
