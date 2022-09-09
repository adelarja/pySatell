from pathlib import Path
from typing import Generator
import geopandas
import itertools


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
        raise(ShapeFileNotFoundException)

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

