import array
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import List
from numpy import ndarray
from pathlib import Path


import numpy as np
import rasterio


class Platform(Enum):
    SENTINEL_2_A = 'S2A'
    SENTINEL_2_B = 'S2B'


class Sensor(Enum):
    MSIL1C = 'MSIL1C'
    MSIL2A = 'MSIL2A'


class BandNumber(Enum):
    B0 = 'B0'
    B01 = 'B01'
    B02 = 'B02'
    B03 = 'B03'
    B04 = 'B04'
    B05 = 'B05'
    B06 = 'B06'
    B07 = 'B07'
    B08 = 'B08'
    B09 = 'B09'
    B10 = 'B10'
    B11 = 'B11'
    B12 = 'B12'
    B8A = 'B13'


@dataclass
class Band:
    number: BandNumber
    resolution: int
    raster: ndarray


@dataclass
class Bands:
    B01: Band = None
    B02: Band = None
    B03: Band = None
    B04: Band = None
    B05: Band = None
    B06: Band = None
    B07: Band = None
    B08: Band = None
    B09: Band = None
    B10: Band = None
    B11: Band = None
    B12: Band = None
    B8A: Band = None


def get_sentinel2_bands(resolution: int, data_path: Path) -> Bands:
    images_paths = data_path.glob(f'**/*B*_{resolution}m.jp2')

    bands = {}

    for image in images_paths:
        band = str(image).split('_')[-2]

        with rasterio.open(image) as f:
            bands[band] = Band(
                BandNumber(band),
                resolution,
                f.read(1)
            )

    return Bands(**bands)


class Sentinel2Bands:

    def __init__(self, filepath: Path):
        acquisition_info = filepath.name.split('_')

        self.platform = Platform(acquisition_info[0])
        self.sensor = Sensor(acquisition_info[1])
        self.date = datetime.strptime(acquisition_info[2], "%Y%m%dT%H%M%S")
        self.data_path = filepath

    def get_ndvi_raster(self):
        np.seterr(divide='ignore', invalid='ignore')
        bands = get_sentinel2_bands(10, self.data_path)

        band_nir = bands.B08.raster
        band_red = bands.B04.raster

        return (
                (band_nir.astype(float) - band_red.astype(float))
                / (band_nir.astype(float) + band_red.astype(float))
        )
