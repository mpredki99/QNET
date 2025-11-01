# Coding: UTF-8

# Copyright (C) 2025 Michał Prędki
# Licensed under the GNU General Public License v3.0.
# Full text of the license can be found in the LICENSE file in the repository.

from pathlib import Path
from typing import Optional

import pandas as pd
import pysurv as ps
from qgis.core import (
    QgsCoordinateTransformContext,
    QgsDataProvider,
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
from .results.output_result import OutputResult
from .results.result import Result


class QGisModel:
    def __init__(self) -> None:
        self._points_data = None
        self._layer = None
        self._data_provider = None

    @property
    def points_data(self) -> Optional[pd.DataFrame]:
        return self._points_data

    @property
    def layer(self) -> Optional[QgsVectorLayer]:
        return self._layer

    @property
    def data_provider(self) -> Optional[QgsDataProvider]:
        return self._data_provider

    @property
    def geometry_type(self) -> Optional[str]:
        if self.points_data is None:
            return
        return "PointZ" if "z" in self.points_data.columns else "Point"

    @property
    def crs(self) -> Optional[str]:
        crs = getattr(self.points_data, "crs", None)
        epsg = crs.to_epsg() if crs else None
        return f"crs=EPSG:{epsg}" if epsg else ""

    def create_output_layer(
        self, project: ps.Project, output_params: OutputParams
    ) -> Result:
        try:
            self._points_data = project.adjustment.report.controls_information_table
            self._create_layer(
                output_params.output_path
                if output_params.output_path
                else "Adjusted_points"
            )
            QgsProject.instance().addMapLayer(self.layer)

            return OutputResult.success("Output layer created.", output=self.layer)

        except Exception as err:
            return OutputResult.error(str(err))

    def create_output_file(
        self, project: ps.Project, output_params: OutputParams
    ) -> Result:
        try:
            self._points_data = project.dataset.controls
            filepath = Path(output_params.output_path)
            self._create_layer(filepath.stem)
            # Add file extension if needed
            if not filepath.suffix == ".shp":
                filepath = filepath.with_suffix(".shp")

            # Remove existing file if needed
            for ext in [".shp", ".shx", ".dbf", ".prj", ".cpg"]:
                filepath.with_suffix(ext).unlink(missing_ok=True)

            # Create options
            options = QgsVectorFileWriter.SaveVectorOptions()
            options.driverName = "ESRI Shapefile"
            options.fileEncoding = "UTF-8"
            options.actionOnExistingFile = QgsVectorFileWriter.CreateOrOverwriteFile

            # Write the layer file
            error = QgsVectorFileWriter.writeAsVectorFormatV2(
                self.layer, str(filepath), QgsCoordinateTransformContext(), options
            )

            if error[0] != QgsVectorFileWriter.NoError:
                return OutputResult.error(str(error[0]))

            shp_layer = QgsVectorLayer(str(filepath), str(filepath.stem), "ogr")
            QgsProject.instance().addMapLayer(shp_layer)

            return OutputResult.success("Output layer file created.", output=shp_layer)

        except Exception as err:
            return OutputResult.error(str(err))

    def _create_layer(self, layer_name: str) -> QgsVectorLayer:
        """Create QGIS layer object."""
        self._layer = QgsVectorLayer(
            f"{self.geometry_type}?{self.crs}", layer_name, "memory"
        )
        self._data_provider = self.layer.dataProvider()

        self._create_layer_fields()
        self._create_layer_features()

    def _create_layer_fields(self) -> None:
        fields = QgsFields()
        # Create index field
        id_field = QgsField("id", QVariant.String)
        fields.append(id_field)
        # Create attributes field
        for col in self.points_data.columns:
            dtype = self.get_field_dtype(self.points_data[col])
            field = QgsField(col, dtype)
            fields.append(field)

        self.data_provider.addAttributes(fields)
        self.layer.updateFields()

    def _create_layer_features(self) -> None:
        feats = []

        for row in self.points_data.itertuples():
            feat = QgsFeature()
            x = getattr(row, "x")
            y = getattr(row, "y")
            z = getattr(row, "z", None)

            geom = (
                QgsGeometry.fromPoint(QgsPoint(x, y, z))
                if z is not None
                else QgsGeometry.fromPointXY(QgsPointXY(x, y))
            )
            feat.setGeometry(geom)
            feat.setAttributes(list(row))
            feats.append(feat)

        self.data_provider.addFeatures(feats)
        self.layer.updateExtents()

    @staticmethod
    def get_field_dtype(column: pd.Series) -> QVariant:
        dtype = column.dtype
        if pd.api.types.is_integer_dtype(dtype):
            return QVariant.Int
        if pd.api.types.is_float_dtype(dtype):
            return QVariant.Double
        if pd.api.types.is_bool_dtype(dtype):
            return QVariant.Bool
        if pd.api.types.is_datetime64_any_dtype(dtype):
            return QVariant.DateTime
        return QVariant.String
