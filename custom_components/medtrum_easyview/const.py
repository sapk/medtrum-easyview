"""Constants for Medtrum EasyView."""

from enum import IntEnum, StrEnum
from logging import Logger, getLogger

LOGGER: Logger = getLogger(__package__)

NAME = "Medtrum EasyView"
DOMAIN = "medtrum_easyview"
VERSION = "1.0.2"
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
REFRESH_RATE_MIN = 1
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

    # From state2 array in the JS code
    DELIVERING_BASAL = 32
    DELIVERING_BASAL_ALT = 33  # Second "Delivering Basal" entry

    # From state3 array (64-79 range)
    LOW_SUSPEND = 64
    PREDICTIVE_LOW_SUSPEND = 65
    AUTO_OFF = 66
    EXCEEDS_MAX_1_HOUR_DELIVERY = 67
    EXCEEDS_MAX_TDD = 68
    SUSPEND = 69

    # From state4 array (96-103 range)
    OCCLUSION_DETECTED = 96
    PATCH_EXPIRED = 97
    EMPTY_RESERVOIR = 98
    PATCH_ERROR_1 = 99
    PATCH_ERROR_2 = 100
    PUMP_BASE_ERROR = 101
    PATCH_BATTERY_DEPLETED = 102
    MAGNETIC_SENSOR_NOT_CALIBRATED = 103

    # From state1 array (0-6 range)
    TO_BE_FILLED = 1
    FILLED_WITH_INSULIN = 2
    PRIMING = 3
    PRIMING_COMPLETED = 4
    INSERTING_NEEDLE = 5
    PATCH_ACTIVATED = 6

    # Special states
    DELIVERY_STOPPED = 128
