# Coding: UTF-8

# Copyright (C) 2025 Michał Prędki
# Licensed under the GNU General Public License v3.0.
# Full text of the license can be found in the LICENSE and COPYING files in the repository.

from __future__ import annotations

from typing import ClassVar, Optional

from pydantic import BaseModel, Field, validator

from ._validators import validate_sigma


class MeasurementModel(BaseModel):
    """
    Model representing a measurement record in a measurements dataset.

    This model is used to validate information about a single measurement row,
    including station and target identifiers, measured values (distances, angles, coordinate differences),
    and their associated standard deviations.
    """

    stn_pk: int
    trg_id: str
    trg_h: Optional[float] = None
    trg_sh: Optional[float] = Field(
        default=None, description="Standard deviation in trg_h."
    )
    sd: Optional[float] = Field(default=None, description="Slope distance.")
    hd: Optional[float] = Field(default=None, description="Horizontal distance.")
    vd: Optional[float] = None
    dx: Optional[float] = None
    dy: Optional[float] = None
    dz: Optional[float] = None
    ssd: Optional[float] = Field(default=None, description="Standard deviation in sd.")
    shd: Optional[float] = Field(default=None, description="Standard deviation in hd.")
    svd: Optional[float] = Field(default=None, description="Standard deviation in vd.")
    sdx: Optional[float] = Field(default=None, description="Standard deviation in dx.")
    sdy: Optional[float] = Field(default=None, description="Standard deviation in dy.")
    sdz: Optional[float] = Field(default=None, description="Standard deviation in dz.")
    a: Optional[float] = None
    hz: Optional[float] = None
    vz: Optional[float] = None
    vh: Optional[float] = None
    sa: Optional[float] = Field(default=None, description="Standard deviation in a.")
    shz: Optional[float] = Field(default=None, description="Standard deviation in hz.")
    svz: Optional[float] = Field(default=None, description="Standard deviation in vz.")
    svh: Optional[float] = Field(default=None, description="Standard deviation in vh.")

    @validator(
        "trg_sh",
        "ssd",
        "shd",
        "svd",
        "sdx",
        "sdy",
        "sdz",
        "sa",
        "shz",
        "svz",
        "svh",
        allow_reuse=True,
    )
    def validate_sigma(cls, v):
        """Validate sigma fields for non-negative values."""
        return validate_sigma(v)

    @validator("sd", "hd", allow_reuse=True)
    def validate_distance(cls, v):
        """Validate that distance values are non-negative."""
        return validate_sigma(v, error_message="Distance values must be >= 0.")

    COLUMN_LABELS: ClassVar[dict] = {
        "station_key": ["stn_pk"],
        "points_label": ["stn_id", "trg_id"],
        "points_height": ["stn_h", "trg_h"],
        "points_height_sigma": ["stn_sh", "trg_sh"],
        "linear_measurements": ["sd", "hd", "vd", "dx", "dy", "dz"],
        "linear_measurements_sigma": ["ssd", "shd", "svd", "sdx", "sdy", "sdz"],
        "angular_measurements": ["a", "hz", "vz", "vh"],
        "angular_measurements_sigma": ["sa", "shz", "svz", "svh"],
    }


class ControlPointModel(BaseModel):
    """
    Model representing a control point in controls dataset.

    This model is used to validate information about a control point,
    including its identifier, coordinates, and associated standard deviations.
    """

    id: str
    x: Optional[float] = None
    y: Optional[float] = None
    z: Optional[float] = None
    sx: Optional[float] = Field(default=None, description="Standard deviation in x.")
    sy: Optional[float] = Field(default=None, description="Standard deviation in y.")
    sz: Optional[float] = Field(default=None, description="Standard deviation in z.")

    @validator("sx", "sy", "sz", allow_reuse=True)
    def validate_sigma(cls, v):
        """Validate sigma fields for non-negative values enabling special value -1."""
        validate_sigma(v, enable_minus_one=True)

    COLUMN_LABELS: ClassVar[dict] = {
        "point_label": ["id"],
        "coordinates": ["x", "y", "z"],
        "sigma": ["sx", "sy", "sz"],
    }


class StationModel(BaseModel):
    """
    Model representing a station record in stations dataset.

    This model is used to validate information about a station,
    including its primary key, identifier, height, standard deviation of height,
    and orientation.
    """

    stn_pk: int
    stn_id: str
    stn_h: Optional[float] = None
    stn_sh: Optional[float] = Field(
        default=None, description="Standard deviation in stn_h."
    )
    orientation: Optional[float] = None

    COLUMN_LABELS: ClassVar[dict] = {
        "station_key": ["stn_pk"],
        "base_point": ["stn_id"],
        "station_attributes": ["stn_h", "stn_sh", "orientation"],
    }

    @validator("stn_sh", allow_reuse=True)
    def validate_sigma(cls, v):
        """Validate stn_sh field for non-negative values."""
        return validate_sigma(v)
