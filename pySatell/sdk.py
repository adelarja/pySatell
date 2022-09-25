from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from pySatell import sentinel_api
from pySatell.models import Bands


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

    def get_indexes(self, date: datetime):
        msi_manager = self.create_msi_image_manager()
        new_images = msi_manager.check_for_new_images(date)

        if new_images:
            msi_manager.download_images(date)
            bands = msi_manager.get_msi_bands()

            indexes = [
                index for index in dir(Bands) if callable(getattr(Bands, index)) and index.startswith('__') is False
            ]

            return [bands.__getattribute__(index)() for index in indexes]


class SentinelMSIManagerCreator(MSIManagerCreator):

    def create_msi_image_manager(self):
        pass


class LandsatMSIManagerCreator(MSIManagerCreator):

    def create_msi_image_manager(self):
        pass


class MSIManager(ABC):
    def __init__(self, filters: Filter):
        self.filters = filters

    @abstractmethod
    def check_for_new_images(self, date: datetime):
        pass

    @abstractmethod
    def download_images(self, date: datetime):
        pass

    @abstractmethod
    def get_msi_bands(self, msi_data_path: Path):
        pass


class SentinelMSIManager(MSIManager):

    def check_for_new_images(self, date: datetime):
        pass

    def download_images(self, date: datetime):
        pass

    def get_msi_bands(self, msi_data_path: Path):
        pass


class LandsatMSIManager(MSIManager):

    def check_for_new_images(self, date: datetime):
        pass

    def download_images(self, date: datetime):
        pass

    def get_msi_bands(self, msi_data_path: Path):
        pass
