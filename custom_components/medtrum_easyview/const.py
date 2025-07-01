"""Constants for Medtrum EasyView."""

from enum import StrEnum
from logging import Logger, getLogger

LOGGER: Logger = getLogger(__package__)

NAME = "Medtrum EasyView"
DOMAIN = "medtrum_easyview"
VERSION = "0.0.0"
ATTRIBUTION = "Data provided by https://easyview.medtrum.eu"
LOGIN_URL = "/v3/api/v2.0/login"
STATUS_URL = "/api/v2.1/monitor/$userid/status"
APP_TAG = "v=3.0.2(15);n=eyvw"
COUNTRY = "Country"
COUNTRY_LIST = [
    "Global"
    "Europe",
    "France",
]
BASE_URL_LIST = {
    "Global": "https://easyview.medtrum.eu",
    "Europe": "https://easyview.medtrum.eu",
    "France": "https://easyview.medtrum.fr",
}
CONTENT_TYPE = "application/json"
GLUCOSE_VALUE_ICON = "mdi:diabetes"
MMOL_L = "mmol/L"
MG_DL = "mg/dL"
MMOL_DL_TO_MG_DL = 18
REFRESH_RATE_MIN = 5
API_TIME_OUT_SECONDS = 20


class DeviceType(StrEnum):
    """Device type enum."""
    
    PUMP = "pump"
    SENSOR = "sensor"
