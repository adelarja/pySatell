from sentinelsat import SentinelAPI

from data import config


sentinel_api = SentinelAPI(config.API_USER, config.API_PASSWORD, config.SENTINEL_API_URL)
