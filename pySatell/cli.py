import typer

from pathlib import Path

from utils import generate_geojsons

app = typer.Typer(help="CLI used to manage satellite images data.")


@app.command
def shp_to_geojson(
        path: str = typer.Argument(
            '.',
            help='Path of the directory containing the shp files to convert.',
            metavar='path'
        )
):
    """Convert shape to geojson."""
    generate_geojsons(Path(path))


@app.command
def get_vegetation_indexes(
        image_path: str = typer.Argument(
            '.',
            help='Path of the directory containing the satellite images.',
            metavar='image_path'
        ),
        fields_path: str = typer.Argument(
            '.',
            help='Path of the directory containing the shapefiles of the desired fields.'
        )
):
    """Get all vegetation indexes for the desired images."""



if __name__ == '__main__':
    app()
