from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import List
from pathlib import Path


class Platform(Enum):
    SENTINEL_2_A = 'S2A'
    SENTINEL_2_B = 'S2B'


class Sensor(Enum):
    MSIL1C = 'MSIL1C'
    MSIL2A = 'MSIL2A'


class BandNumber(Enum):
    B0 = 0
    B1 = 1
    B2 = 2
    B3 = 3
    B4 = 4
    B5 = 5
    B6 = 6
    B7 = 7
    B8 = 8
    B9 = 9
    B10 = 10
    B11 = 11
    B12 = 12
    B8A = 13


@dataclass
class Band:
    number: BandNumber
    resolution: int
    raster: int


@dataclass
class Bands:
    B1: Band = None
    B2: Band = None
    B3: Band = None
    B4: Band = None
    B5: Band = None
    B6: Band = None
    B7: Band = None
    B8: Band = None
    B9: Band = None
    B10: Band = None
    B11: Band = None
    B12: Band = None
    B8A: Band = None


class Sentinel2Bands:
    platform: Platform
    date: datetime
    sensor: Sensor
    bands10m: Bands
    bands20m: Bands
    bands60m: Bands

    def __init__(self, filepath: Path):
        acquisition_info = filepath.name.split('_')

        self.platform = Platform(acquisition_info[0])
        self.sensor = Sensor(acquisition_info[1])
        self.date = datetime.strptime(acquisition_info[2], "%Y%m%dT%H%M%S")
        self.data_path = filepath

    def get_ndvi_raster(self):
        pass
