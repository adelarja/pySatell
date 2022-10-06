import typer

import matplotlib
import matplotlib.pyplot as plt

from pathlib import Path

from plotter import IndexPlotter
from sdk import LandsatMSIManagerCreator, SentinelMSIManagerCreator, SentinelProcessingParams, Fields
from utils import generate_geojsons

app = typer.Typer(help="CLI used to manage satellite images data.")


@app.command()
def shp_to_geojson(
        path: str = typer.Argument(
            '.',
            help='Path of the directory containing the shp files to convert.',
            metavar='path'
        )
):
    """Convert shape to geojson."""
    generate_geojsons(Path(path))


@app.command()
def get_vegetation_indexes(
        image_path: str = typer.Argument(
            '.',
            help='Path of the directory containing the satellite images.',
            metavar='image_path'
        ),
        fields_path: str = typer.Argument(
            '.',
            help='Path of the directory containing the shapefiles of the desired fields.'
        ),
        sentinel: bool = typer.Option(
            False,
            help='Process sentinel images.',
            metavar='sentinel'
        ),
        landsat: bool = typer.Option(
            False,
            help='Process landsat images.',
            metavar='landsat'
        )

):
    """Get all vegetation indexes for the desired images."""

    if sentinel:
        fields = Fields(Path(fields_path))
        filters = SentinelProcessingParams(
            data_path=Path(image_path),
            fields=fields,
            resolution=10
        )
        manager = SentinelMSIManagerCreator()
    elif landsat:
        manager = LandsatMSIManagerCreator()
        filters = None
    else:
        manager = SentinelMSIManagerCreator()
        filters = None

    indexes = manager.get_indexes(filters)

    for band in indexes:
        band = band[0]
        band2 = band.copy()

        band[band <= 0] = 0
        band[(band > 0) & (band <= 0.1)] = 1
        band[(band > 0.1) & (band <= 0.2) & (band < 1)] = 2
        band[(band > 0.2) & (band <= 0.3) & (band < 1)] = 3
        band[(band > 0.3) & (band <= 0.4) & (band < 1)] = 4
        band[(band > 0.4) & (band <= 0.5) & (band < 1)] = 5
        band[(band > 0.5) & (band <= 0.6) & (band < 1)] = 6
        band[(band > 0.6) & (band <= 0.7) & (band < 1)] = 7
        band[(band > 0.7) & (band <= 0.8) & (band < 1)] = 8
        band[(band > 0.8) & (band <= 0.9) & (band < 1)] = 9
        band[(band > 0.9) & (band < 1)] = 10

        plt.imshow(band, cmap='RdYlGn')
        plt.colorbar()
        plt.show()

        plt.imshow(band2, cmap='RdYlGn')
        plt.colorbar()
        plt.show()

    return indexes


@app.command()
def plot_vegetation_indexes(
        image_path: str = typer.Argument(
            '.',
            help='Path of the directory containing the satellite images.',
            metavar='image_path'
        ),
        fields_path: str = typer.Argument(
            '.',
            help='Path of the directory containing the shapefiles of the desired fields.'
        ),
        sentinel: bool = typer.Option(
            False,
            help='Process sentinel images.',
            metavar='sentinel'
        ),
        landsat: bool = typer.Option(
            False,
            help='Process landsat images.',
            metavar='landsat'
        )

):
    """Get all vegetation indexes for the desired images."""

    if sentinel:
        fields = Fields(Path(fields_path))
        filters = SentinelProcessingParams(
            data_path=Path(image_path),
            fields=fields,
            resolution=10
        )
        manager = SentinelMSIManagerCreator()
    elif landsat:
        manager = LandsatMSIManagerCreator()
        filters = None
    else:
        manager = SentinelMSIManagerCreator()
        filters = None

    fields = manager.get_fields(filters)

    for field in fields:
        for index_name, index_raster in field.get_all_indexes().items():
            index_plotter = IndexPlotter(index_raster)

            ndvi_ax = index_plotter('ndvi_plot', ax=None, kws={'cmap': 'RdYlGn'})
            ndvi_ax.plot()
            ndvi_ax.set_title(index_name)
            plt.suptitle(field.farm_name)
            plt.show()

            heat_map_ax = index_plotter('heat_map', ax=None, kws={'cmap': 'RdYlGn'})
            heat_map_ax.plot()
            heat_map_ax.set_title(f'Heatmap for {index_name}')
            plt.suptitle(field.farm_name)
            plt.show()


if __name__ == '__main__':
    app()
