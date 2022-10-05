from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import List, OrderedDict
from numpy import ndarray
from pathlib import Path
from rasterio.mask import mask


import numpy as np
import rasterio
import fiona


class Platform(Enum):
    """Enum used to represent the platform holding the sensor."""
    SENTINEL_2_A = 'S2A'
    SENTINEL_2_B = 'S2B'


class Sensor(Enum):
    """Enum used to represent the different kinds of sensors.

    MSI (Multi Spectral Instrument) is the optical sensor present in the
    sentinel2 a and b platforms.
    """
    MSIL1C = 'MSIL1C'
    MSIL2A = 'MSIL2A'


class BandNumber(Enum):
    """Enum used to represent the band number."""
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
    """Data type used to encapsulate all the information for a single band.

    Attributes:
        number (BandNumber): represents the wavelength of the electromagnetic
            spectrum that is being digitalized by the instrument.
        resolution (int): The pixel resolution (for example, 10 represents a
            10m by 10m pixel resolution).
        raster (ndarray): A numpy array with the band information.
    """
    number: BandNumber
    resolution: int
    raster: ndarray


@dataclass
class Bands:
    """Represents all the bands for a given instrument.

    This class is mainly used to calculate the different indexes using
        bands algebra.
    """
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

    def ndvi(self):
        """Returns the ndvi index."""
        band_nir = self.B08.raster
        band_red = self.B04.raster

        return (
                (band_nir.astype(float) - band_red.astype(float))
                / (band_nir.astype(float) + band_red.astype(float))
        )


@dataclass
class FieldData:
    """Encapsulates all the information of a particular Field.

    Attributes:
        properties (OrderedDict): All the properties contained in
            a shape (shp) file.
        geometry (dict): The geometries obtained from the shp file.
        bands: A band object used for indexes calculations of the field.
    """
    properties: OrderedDict
    geometry: dict
    bands: Bands = None

    @property
    def farm_name(self) -> str:
        """Returns the farm_name if exists in the properties."""
        return self.properties.get('farm_name', "")

    def get_all_indexes(self) -> dict:
        """Returns all indexes for a given bands object.

        Returns:
            A dict with the name of the index as the key and the
                calculated index raster as the value.
        """
        indexes = [
            index for index in dir(Bands) if callable(getattr(Bands, index)) and index.startswith('__') is False
        ]
        calculated_indexes = {}
        for index in indexes:
            calculated_indexes.update({index: self.bands.__getattribute__(index)()})

        return calculated_indexes


class Fields:
    """Represents all the fields that want to be analyzed.

    The __init__ method receives a shape files path of a
        directory containing all the shape files of the
        fields that want to be analyzed.

    Args:
        shp_files_path (Path): A Path object of a directory
            containing the shapefiles of the fields that
            want to be analyzed.

    Attributes:
        fields (List[FieldData]): All the Field objects
            with information about the fields.
    """

    def __init__(self, shp_files_path: Path):
        fiona_geometries = []

        for field in shp_files_path.glob('./*.shp'):
            file = fiona.open(field)
            for geometry in file:
                fiona_geometries.append(
                    FieldData(
                        properties=geometry['properties'], geometry=geometry['geometry']
                    )
                )

        self.fields = fiona_geometries


def get_sentinel2_bands(resolution: int, data_path: Path, fields_path: Path) -> List[Bands]:
    """Get the sentinel 2 bands of a list of fields.

    The method obtain the sentinel2 bands for a particular resolution,
        it clips the rasters using the field boundaries information,
        and returns a list of Bands objects representing each of the
        fields data.

    Args:
        resolution (int): The bands resolution in meters.
            It can be 10, 20 or 60.
        data_path (Path): Path object where the sentinel2
            bands information is located.
        fields_path (Path): Directory path with the shp files
            representing the fields that want to be analyzed.

    Returns:
        A List[Bands] object each one representing a field's band.
    """
    clipped_rasters = []
    fields = Fields(fields_path)

    for field in fields.fields:

        bands = {}
        images_paths = data_path.glob(f'**/*B*_{resolution}m.jp2')

        for image in images_paths:
            band = str(image).split('_')[-2]

            with rasterio.open(image) as f:

                clipped_band, _ = mask(f, [field], crop=True)

                bands[band] = Band(
                    BandNumber(band),
                    resolution,
                    clipped_band
                )

        clipped_rasters.append(Bands(**bands))

    return clipped_rasters


class Sentinel2Bands:

    def __init__(self, filepath: Path, fields_path: Path = None):
        acquisition_info = filepath.name.split('_')

        self.platform = Platform(acquisition_info[0])
        self.sensor = Sensor(acquisition_info[1])
        self.date = datetime.strptime(acquisition_info[2], "%Y%m%dT%H%M%S")
        self.data_path = filepath
        self.fields_path = fields_path

    def get_ndvi_raster(self):
        np.seterr(divide='ignore', invalid='ignore')
        fields_bands = get_sentinel2_bands(10, self.data_path, self.fields_path)

        fields_ndvi = []

        for field_bands in fields_bands:

            fields_ndvi.append(field_bands.ndvi)

        return fields_ndvi
