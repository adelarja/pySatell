from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path


class MSIManagerCreator(ABC):

    @abstractmethod
    def create_msi_image_manager(self):
        pass


class SentinelMSIManagerCreator(MSIManagerCreator):

    def create_msi_image_manager(self):
        pass


class LandsatMSIManagerCreator(MSIManagerCreator):

    def create_msi_image_manager(self):
        pass


class MSIManager(ABC):

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
