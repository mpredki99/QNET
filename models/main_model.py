# Coding: UTF-8

# Copyright (C) 2025 Michał Prędki
# Licensed under the GNU General Public License v3.0.
# Full text of the license can be found in the LICENSE file in the repository.

from dataclasses import dataclass, field

from .pysurv_model import PySurvModel
from .qgis_model import QGisModel


@dataclass
class MainModel:
    pysurv_model: PySurvModel = field(default_factory=PySurvModel)
    qgis_model: QGisModel = field(default_factory=QGisModel)
