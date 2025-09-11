# Coding: UTF-8

# Copyright (C) 2025 Michał Prędki
# Licensed under the GNU General Public License v3.0.
# Full text of the license can be found in the LICENSE file in the repository.

from enum import Enum, auto
from typing import Tuple


class robust(Enum):
    """Temporary mock real robust module import from pysurv package - from pysurv import robust"""

    huber = auto()
    slope = auto()
    hampel = auto()
    danish = auto()
    epanechnikov = auto()
    tukey = auto()
    jacobi = auto()
    exponential = auto()
    cra = auto()
    error_func = auto()
    cauchy = auto()
    t = auto()
    bell = auto()
    chain = auto()
    andrews = auto()
    wave = auto()
    half_wave = auto()
    wigner = auto()
    ellipse_curve = auto()
    trim = auto()


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
    "Bell Curve": robust.bell,
    "Chain Curve": robust.chain,
    "Andrews": robust.andrews,
    "Wave": robust.wave,
    "Half-wave": robust.half_wave,
    "Wigner": robust.wigner,
    "Ellipse Curve": robust.ellipse_curve,
    "Trim": robust.trim,
}


def get_default_tuning_constants(func) -> Tuple[float]:
    tuning_constants = {
        robust.huber: (1.345,),
        robust.slope: (2, 2),
        robust.hampel: (1.7, 3.4, 8.5),
        robust.danish: (2.5,),
        robust.epanechnikov: (3.674, 2),
        robust.tukey: (4.685, 2),
        robust.jacobi: (4.687, 1),
        robust.exponential: (2, 2),
        robust.cra: (2, 2),
        robust.error_func: (1.414, 2),
        robust.cauchy: (2.385, 2),
        robust.t: (1, 2),
        robust.bell: (1, 1),
        robust.chain: (1,),
        robust.andrews: (4.207,),
        robust.wave: (2.5,),
        robust.half_wave: (2.5,),
        robust.wigner: (3.137,),
        robust.ellipse_curve: (2.5,),
        robust.trim: (2.5,),
    }

    return tuning_constants.get(func, tuple())
