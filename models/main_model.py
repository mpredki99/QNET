# Coding: UTF-8

# Copyright (C) 2025 Michał Prędki
# Licensed under the GNU General Public License v3.0.
# Full text of the license can be found in the LICENSE file in the repository.

from dataclasses import dataclass, field

from .pysurv_model import PySurvModel
from .qgis_model import QGisModel


@dataclass
class MainModel:
    """
    Central coordinator model for the QNET plugin.

    This class aggregates and provides access to the two sub-models responsible
    for core data processing and QGIS integration: `PySurvModel` and `QGisModel`.
    It serves as the main gateway between the ViewModel layer and the computational or
    spatial logic, enabling execution of PySurv adjustment operations and QGIS data
    exports.

    Attributes
    ----------
    - pysurv_model : PySurvModel
        Handles data import, least squares adjustment, and report generation.
    - qgis_model : QGisModel
        Handles output creation and export to QGIS layers or shapefiles.
    """

    pysurv_model: PySurvModel = field(default_factory=PySurvModel)
    qgis_model: QGisModel = field(default_factory=QGisModel)
