# Coding: UTF-8

# Copyright (C) 2025 Michał Prędki
# Licensed under the GNU General Public License v3.0.
# Full text of the license can be found in the LICENSE file in the repository.

from inspect import signature, unwrap
from typing import Dict

from pysurv.adjustment import robust

WEIGHTING_METHODS = {
    "Ordinary": None,
    "Weighted": None,
    "Huber": robust.huber,
    "Slope": robust.slope,
    "Hampel": robust.hampel,
    "Danish": robust.danish,
    "Epanechnikov": robust.epanechnikov,
    "Tukey": robust.tukey,
    "Jacobi": robust.jacobi,
    "Exponential": robust.exponential,
    "Choice Rule of Alternative": robust.cra,
    "Error Function": robust.error_func,
    "Cauchy": robust.cauchy,
    "T distribution": robust.t,
    "Bell Curve": robust.chain_bell,
    "Chain Curve": robust.chain,
    "Andrews": robust.andrews,
    "Wave": robust.wave,
    "Half-wave": robust.half_wave,
    "Wigner": robust.wigner,
    "Ellipse Curve": robust.ellipse_curve,
    "Trim": robust.trim,
}


def get_default_tuning_constants(func) -> Dict[str, float]:
    if not func:
        return dict()

    wrapped_func = unwrap(func)
    sig = signature(wrapped_func)

    return {
        key: value.default
        for key, value in sig.parameters.items()
        if isinstance(value.default, (int, float))
    }
