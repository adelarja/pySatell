from sentinelsat import SentinelAPI


API_USER = "****"
API_PASSWORD = "****"
SENTINEL_API_URL = 'https://apihub.copernicus.eu/apihub'

sentinel_api = SentinelAPI(API_USER, API_PASSWORD, SENTINEL_API_URL)