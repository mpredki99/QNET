# Coding: UTF-8

# Copyright (C) 2025 Michał Prędki
# Licensed under the GNU General Public License v3.0.
# Full text of the license can be found in the LICENSE file in the repository.

from pathlib import Path
from typing import Optional

import pandas as pd
import pysurv as ps
from pysurv.data import Controls
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
from .results.result import Result, ResultStatus


class QGisModel:
    """
    Model handling QGIS-specific output generation for the QNET plugin.

    This class provides functionality to convert adjusted points data into QGIS layer.
    It creates temporary vector layer or writes shapefile using the QGIS API, managing
    geometry creation, attribute mapping, and CRS assignment.

    Properties
    ----------
    - points_data : Optional[Controls]
        Dataset containing adjusted control points.
    - layer : Optional[QgsVectorLayer]
        QGIS vector layer created during output generation.
    - data_provider : Optional[QgsDataProvider]
        Data provider for adding attributes and features to the layer.
    """

    def __init__(self) -> None:
        """Initialize the QGIS model with empty attribute references."""
        self._points_data: Optional[Controls] = None
        self._layer: Optional[QgsVectorLayer] = None
        self._data_provider: Optional[QgsDataProvider] = None

    @property
    def points_data(self) -> Optional[Controls]:
        """Return the PySurv dataset currently used for generating QGIS layers."""
        return self._points_data

    @property
    def layer(self) -> Optional[QgsVectorLayer]:
        """Return the QGIS vector layer instance."""
        return self._layer

    @property
    def data_provider(self) -> Optional[QgsDataProvider]:
        """Return the data provider for the QGIS layer."""
        return self._data_provider

    @property
    def geometry_type(self) -> Optional[str]:
        """Determine the geometry type based on the dataset columns."""
        if self.points_data is None:
            return
        return "PointZ" if "z" in self.points_data.columns else "Point"

    @property
    def crs(self) -> str:
        """Return the coordinate reference system string for the layer."""
        crs = getattr(self.points_data, "crs", None)
        epsg = crs.to_epsg() if crs else None
        return f"crs=EPSG:{epsg}" if epsg else ""

    def create_output_layer(
        self, project: ps.Project, output_params: OutputParams
    ) -> Result:
        """
        Create a temporary QGIS vector layer from the PySurv adjustment results.

        Uses the adjusted control point data to populate a QGIS memory layer and
        add it to the current QGIS project.

        Parameters
        ----------
        - project : ps.Project
            PySurv project containing adjustment results.
        - output_params : OutputParams
            Output parameters including optional output layer name or file path.

        Returns
        -------
        - Result
            OutputResult indicating layer creation status and optional QGIS point layer.
        """
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
        """
        Export adjusted data to a shapefile and add it to the QGIS project.

        Writes the adjusted coordinates to disk in Shapefile format, managing file
        cleanup and encoding options. Automatically adds the exported layer to the
        QGIS project upon success.

        Parameters
        ----------
        - project : ps.Project
            PySurv project containing adjustment results.
        - output_params : OutputParams
            Output parameters including optional output layer name or file path.

        Returns
        -------
        - Result
            OutputResult indicating shapefile export status and optional QGIS point layer.
        """
        try:
            # Try export temporary file if no output path provided
            if not output_params.output_path:
                temporary_layer_result = self.create_output_layer(project, output_params)
                if temporary_layer_result.status != ResultStatus.ERROR:
                    return OutputResult.error("Empty QGIS layer file path. Temporary layer created.")
                return temporary_layer_result
            
            self._points_data = project.adjustment.report.controls_information_table
            filepath = Path(output_params.output_path)
            self._create_layer(filepath.stem)
            # Add file extension if needed
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
        """
        Create a new QGIS layer and populate it with fields and features.

        Parameters
        ----------
        - layer_name : str
            Name to assign to the created QGIS layer.

        Returns
        -------
        - QgsVectorLayer
            Created QGIS vector layer instance.
        """
        self._layer = QgsVectorLayer(
            f"{self.geometry_type}?{self.crs}", layer_name, "memory"
        )
        self._data_provider = self.layer.dataProvider()

        self._create_layer_fields()
        self._create_layer_features()

    def _create_layer_fields(self) -> None:
        """Create and add attribute fields to the QGIS layer based on dataset columns."""
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
        """Create and add point features to the QGIS layer using dataset geometry data."""
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
        """Map a columns dtype to the corresponding QGIS QVariant type."""
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
