# Coding: UTF-8

# Copyright (C) 2025 Michał Prędki
# Licensed under the GNU General Public License v3.0.
# Full text of the license can be found in the LICENSE file in the repository.

import os

import pysurv as ps
from qgis.core import (
    QgsCoordinateTransformContext,
    QgsFeature,
    QgsField,
    QgsFields,
    QgsGeometry,
    QgsPoint,
    QgsPointXY,
    QgsProject,
    QgsVectorFileWriter,
    QgsVectorLayer,
)
from qgis.PyQt.QtCore import QVariant

from ..dto.data_transfer_objects import OutputParams
from ..qnet_exceptions import OutputError


def create_output_layer(project: ps.Project, output_params: OutputParams):
    """Create QGIS point layer and add it to the QGIS project."""
    try:

        layer = create_layer(project.dataset.controls, output_params.output_path)
        # Add to project
        QgsProject.instance().addMapLayer(layer)
        return layer
    except:
        raise OutputError


def create_output_file(project: ps.Project, output_params: OutputParams):
    """Create file with points geometry and add it to the QGIS project."""
    filepath = output_params.output_path

    if not filepath.lower().endswith(".shp"):
        filepath += ".shp"

    layer_name = os.path.basename(filepath).split(".")[0]
    try:
        layer = create_layer(project.dataset.controls, layer_name)
    except:
        raise OutputError

    # Remove existing file if needed
    for ext in [".shp", ".shx", ".dbf", ".prj", ".cpg"]:
        file = os.path.splitext(filepath)[0] + ext
        if os.path.exists(file):
            os.remove(file)

    # Create options
    options = QgsVectorFileWriter.SaveVectorOptions()
    options.driverName = "ESRI Shapefile"
    options.fileEncoding = "UTF-8"
    options.actionOnExistingFile = QgsVectorFileWriter.CreateOrOverwriteFile

    # Write the layer file
    error = QgsVectorFileWriter.writeAsVectorFormatV2(
        layer, filepath, QgsCoordinateTransformContext(), options
    )

    if error[0] != QgsVectorFileWriter.NoError:
        raise OutputError

    shp_layer = QgsVectorLayer(filepath, layer_name, "ogr")
    QgsProject.instance().addMapLayer(shp_layer)
    return shp_layer


def create_layer(controls, name):

    geometry_type = "PointZ" if "z" in controls.coordinate_columns else "Point"

    epsg = controls.crs.to_epsg() if controls.crs else None
    crs_str = f"crs=EPSG:{epsg}" if epsg else ""

    layer_name = name if name else "Adjusted_points"

    layer = QgsVectorLayer(f"{geometry_type}?{crs_str}", layer_name, "memory")
    provider = layer.dataProvider()

    # Create fields
    fields = QgsFields()
    for col in controls.columns:
        fields.append(QgsField(col, QVariant.Double))

    provider.addAttributes(fields)
    layer.updateFields()

    # Create features
    feats = []
    for _, row in controls.iterrows():
        feat = QgsFeature()
        x, y = float(row["x"]), float(row["y"])
        z = float(row["z"]) if "z" in controls.coordinate_columns else None
        geom = (
            QgsGeometry.fromPoint(QgsPoint(x, y, z))
            if z is not None
            else QgsGeometry.fromPointXY(QgsPointXY(x, y))
        )
        feat.setGeometry(geom)
        feat.setAttributes(list(row))
        feats.append(feat)

    provider.addFeatures(feats)
    layer.updateExtents()
    return layer
