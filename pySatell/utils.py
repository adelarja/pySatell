from pathlib import Path
from typing import Generator, Dict, Tuple, List
from datetime import datetime
from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt
from data import config

import geopandas
import itertools
import zipfile


class ShapefileNotFoundException(Exception):
    pass


def shape_to_geojson(file_path: Path) -> None:
    """This function converts shapefiles to geojson files.

    Args:
        file_path (Path): Posix path of the shapefile.
    """
    shape_file = geopandas.read_file(file_path)
    geojson_file_name = '.'.join(file_path.name.split('.')[:-1] + ['geojson'])
    shape_file.to_file(file_path.parent / geojson_file_name)


def get_shapefiles_generator(directory: Path) -> Generator[Path, None, None]:
    """Get a generator with the shapefiles paths.

    Args:
        directory (Path): Path of a directory containing shapefiles.

    Raises:
        ShapefileNotFoundException if no shapefile is present in the
            directory.
    """
    shapefiles = directory.glob('**/*.shp')

    try:
        first = next(shapefiles)
    except StopIteration:
        raise ShapefileNotFoundException

    return itertools.chain([first], shapefiles)


def generate_geojsons(directory: Path) -> None:
    """Generate geojson files for all the shapefiles in a directory.

    Args:
        directory (Path): A path containing the shapefiles to convert.

    Raises:
        ShapeFileNotFoundException when no shapefile is present in the directory.
    """
    shapefiles = get_shapefiles_generator(directory)

    for shapefile in shapefiles:
        shape_to_geojson(shapefile)


def get_products_by_date_and_area(
        date_from: datetime,
        date_to: datetime,
        geojson_path: Path,
        platform_name: str,
        cloud_coverage_percentage: Tuple = (0, 100)
) -> Dict[str, dict]:
    """Gets the available products for a specific date and specifics coordinates.

    Args:
        date_from (datetime): Starting date for the time window whose information
            wants to be retrieved.

        date_to (datetime): End date for the time window whose information
            wants to be retrieved.

        geojson_path (Path): A path object of a geojson file with information about
            the coordinates of the desired area.

        platform_name (str): The name of the satellite that obtain the images. For example,
            if we want to obtain optical images, we could pass 'Sentinel-2' as platform_name.

        cloud_coverage_percentage (Tuple): Percentage of cloud coverage of S2 products for
            each area covered by a reference band. Possible values go from 0 to 100.

    Returns:
        An OrderedDict with information of all the available products for the desired
            date and area.
    """
    api = SentinelAPI(config.API_USER, config.API_PASSWORD, config.SENTINEL_API_URL)

    footprint = geojson_to_wkt(read_geojson(geojson_path))
    products = api.query(
        footprint,
        date=(datetime.strftime(date_from, "%Y%m%d"), date_to.date()),
        platformname=platform_name,
        cloudcoverpercentage=cloud_coverage_percentage
    )

    return products


def unzip_sentinel2_data(directory: Path) -> None:
    """Unzip all the zip files containing sentinel 2 data in a directory.

    Args:
        directory (Path): Path of a directory containing the zip files to
            extract.
    """
    zipfiles = directory.glob('**/*.zip')

    for zipfile_ in zipfiles:
        with zipfile.ZipFile(zipfile_, 'r') as zip_ref:
            zip_ref.extractall(directory)
