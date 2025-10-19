# Coding: UTF-8

# Copyright (C) 2025 Michał Prędki
# Licensed under the GNU General Public License v3.0.
# Full text of the license can be found in the LICENSE file in the repository.

from typing import Protocol

import pysurv as ps

from ..dto.data_transfer_objects import OutputParams


class QGisModel(Protocol):
    def create_output_layer(self, project: ps.Project, output_params: OutputParams):
        """Create QGIS point layer and add it to the QGIS project."""
        ...

    def create_output_file(self, project: ps.Project, output_params: OutputParams):
        """Create file with points geometry and add it to the QGIS project."""
        ...
