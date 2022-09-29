import rasterio

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from data import sentinel_api
from models import Band, BandNumber, Bands, Fields

from sentinelsat import geojson_to_wkt
from rasterio.mask import mask


@dataclass
class QueryParams:
    date_from: datetime
    date_to: datetime
    desired_zone: dict


@dataclass
class SentinelQueryParams(QueryParams):
    platform_name: str = 'Sentinel-2'
    cloud_coverage_percentage: tuple = (0, 100)


@dataclass
class ProcessingParams:
    data_path: Path
    fields: Fields


@dataclass
class SentinelProcessingParams(ProcessingParams):
    resolution: int


@dataclass
class Filter:
    date_from: datetime
    date_to: datetime


@dataclass
class SentinelFilter(Filter):
    cloud_coverage_percentage: tuple = (0, 100)


class MSIManagerCreator(ABC):

    @abstractmethod
    def create_msi_image_manager(self):
        pass

    def get_indexes(self, processing_params: ProcessingParams):
        msi_manager = self.create_msi_image_manager()
        bands = msi_manager.get_msi_bands(processing_params)
        indexes = [
            index for index in dir(Bands) if callable(getattr(Bands, index)) and index.startswith('__') is False
        ]
        calculated_indexes = []
        for index in indexes:
            for band in bands:
                calculated_indexes.append(band.__getattribute__(index)())

        return calculated_indexes

    def get_new_indexes(self, query_params: QueryParams, processing_params: ProcessingParams):
        msi_manager = self.create_msi_image_manager()
        new_images = msi_manager.download_new_images(query_params.desired_zone)

        if new_images:
            msi_manager.download_images(query_params.desired_zone)
            bands = msi_manager.get_msi_bands(processing_params)

            indexes = [
                index for index in dir(Bands) if callable(getattr(Bands, index)) and index.startswith('__') is False
            ]

            calculated_indexes = []
            for index in indexes:
                for band in bands:
                    calculated_indexes.append(band.__getattribute__(index)())

            return calculated_indexes


class SentinelMSIManagerCreator(MSIManagerCreator):

    def create_msi_image_manager(self):
        return SentinelMSIManager()


class LandsatMSIManagerCreator(MSIManagerCreator):

    def create_msi_image_manager(self):
        return LandsatMSIManager()


class MSIManager(ABC):

    @abstractmethod
    def download_new_images(self, query_params: QueryParams):
        pass

    @abstractmethod
    def get_msi_bands(self, processing_params: ProcessingParams):
        pass


class SentinelMSIManager(MSIManager):

    def download_new_images(self, query_params: SentinelQueryParams):
        footprint = geojson_to_wkt(query_params.desired_zone)

        products = sentinel_api.query(
            footprint,
            date=(
                datetime.strftime(query_params.date_from, "%Y%m%d"),
                query_params.date_to.date()
            ),
            platformname=query_params.platform_name,
            cloudcoverpercentage=query_params.cloud_coverage_percentage
        )

        sentinel_api.download_all(products)

    def get_msi_bands(self, processing_params: SentinelProcessingParams):
        clipped_rasters = []

        for field in processing_params.fields.fields:

            bands = {}
            images_paths = processing_params.data_path.glob(f'**/*B*_{processing_params.resolution}m.jp2')

            for image in images_paths:
                band = str(image).split('_')[-2]

                with rasterio.open(image) as f:
                    clipped_band, _ = mask(f, [field], crop=True)

                    bands[band] = Band(
                        BandNumber(band),
                        processing_params.resolution,
                        clipped_band
                    )

            clipped_rasters.append(Bands(**bands))

        return clipped_rasters


class LandsatMSIManager(MSIManager):

    def download_new_images(self, query_params: QueryParams):
        pass

    def get_msi_bands(self, processing_params: ProcessingParams):
        pass
