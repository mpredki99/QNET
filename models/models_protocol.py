# Coding: UTF-8

# Copyright (C) 2025 Michał Prędki
# Licensed under the GNU General Public License v3.0.
# Full text of the license can be found in the LICENSE file in the repository.

from typing import Protocol

from .pysurv_model_protocol import PySurvModel
from .qgis_model_protocol import QGisModel


class Models(Protocol):
    pysurv_model: PySurvModel
    qgis_model: QGisModel
