"""Constants for Medtrum EasyView."""

from enum import IntEnum, StrEnum
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
    "GlobalEurope",
    "France",
]
BASE_URL_LIST = {
    "Global": "https://easyview.medtrum.eu",
    "Europe": "https://easyview.medtrum.eu",
    "France": "https://easyview.medtrum.fr",
}
CONTENT_TYPE = "application/json"
MMOL_L = "mmol/L"
MG_DL = "mg/dL"
MMOL_DL_TO_MG_DL = 18
REFRESH_RATE_MIN = 5
API_TIME_OUT_SECONDS = 20

# Icons
GLUCOSE_VALUE_ICON = "mdi:diabetes"
PUMP_ICON = "mdi:needle"
PUMP_ON_ICON = "mdi:water-sync"
PUMP_OFF_ICON = "mdi:water-off"
SENSOR_ICON = "mdi:diabetes"
CLOCK_ICON = "mdi:clock"
TIMELINE_ICON = "mdi:timeline-clock"
BASAL_ICON = "mdi:water-sync"
BOLUS_ICON = "mdi:water-plus"
VOLUME_ICON = "mdi:gauge"
REMAINING_TIME_ICON = "mdi:clock-end"


class DeviceType(StrEnum):
    """Device type enum."""

    PUMP = "pump"
    SENSOR = "sensor"


class PumpStatus(IntEnum):
    """Pump status enum."""

    DELIVERING_BASAL = 32
