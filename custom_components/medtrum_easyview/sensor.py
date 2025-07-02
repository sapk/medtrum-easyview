"""Sensor platform for Medtrum EasyView."""

from __future__ import annotations

import logging
from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.const import CONF_UNIT_OF_MEASUREMENT

from .const import (
    BASAL_ICON,
    BOLUS_ICON,
    CLOCK_ICON,
    DOMAIN,
    GLUCOSE_VALUE_ICON,
    MG_DL,
    PUMP_ICON,
    REMAINING_TIME_ICON,
    SENSOR_ICON,
    TIMELINE_ICON,
    VOLUME_ICON,
    DeviceType,
    PumpStatus,
)
from .device import MedtrumEasyViewDevice

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .coordinator import MedtrumEasyViewDataUpdateCoordinator

# GVS: Tuto pour ajouter des log
_LOGGER = logging.getLogger(__name__)

""" Three sensors are declared:
    Glucose Value
    Glucose Trend
    Sensor days and related sensor attributes"""


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]

    # If custom unit of measurement is selected, otherwise MG/DL is used
    try:
        custom_unit = config_entry.data[CONF_UNIT_OF_MEASUREMENT]
    except KeyError:
        custom_unit = MG_DL

    sensors = [
        MedtrumEasyViewSensor(
            coordinator,
            DeviceType.PUMP,
            SensorDeviceClass.ENUM,
            None,
            "status",  # key
            "Pump Status",  # name
            PUMP_ICON,
            None,
            None,
        ),
        MedtrumEasyViewSensor(
            coordinator,
            DeviceType.PUMP,
            SensorDeviceClass.DURATION,
            SensorStateClass.MEASUREMENT,
            "remainingTime",  # key
            "Pump Remaining time",  # name
            REMAINING_TIME_ICON,
            "min",
            "d",
        ),
        MedtrumEasyViewSensor(
            coordinator,
            DeviceType.PUMP,
            None,
            SensorStateClass.MEASUREMENT,
            "remainingDose",  # key
            "Pump Remaining dose",  # name
            VOLUME_ICON,
            "U",
            None,
        ),
        MedtrumEasyViewSensor(
            coordinator,
            DeviceType.PUMP,
            SensorDeviceClass.TIMESTAMP,
            None,
            "updateTime",  # key
            "Pump Last update",  # name
            CLOCK_ICON,
            None,
            None,
        ),
        MedtrumEasyViewSensor(
            coordinator,
            DeviceType.PUMP,
            SensorDeviceClass.BLOOD_GLUCOSE_CONCENTRATION,
            None,
            "bGTarget",  # key
            "Blood Glucose Target",  # name
            GLUCOSE_VALUE_ICON,
            custom_unit,
            None,
        ),
        MedtrumEasyViewSensor(
            coordinator,
            DeviceType.PUMP,
            None,
            SensorStateClass.TOTAL_INCREASING,
            "basalSum",  # key
            "Basal Daily Volume",  # name
            BASAL_ICON,
            "U",
            None,
        ),
        MedtrumEasyViewSensor(
            coordinator,
            DeviceType.PUMP,
            None,
            SensorStateClass.TOTAL_INCREASING,
            "bolusSum",  # key
            "Bolus Daily Volume",  # name
            BOLUS_ICON,
            "U",
            None,
        ),
        MedtrumEasyViewSensor(
            coordinator,
            DeviceType.PUMP,
            None,
            SensorStateClass.MEASUREMENT,
            "basalRate",  # key
            "Basal Rate",  # name
            BASAL_ICON,
            "U/h",
            None,
        ),
        MedtrumEasyViewSensor(
            coordinator,
            DeviceType.PUMP,
            SensorDeviceClass.TIMESTAMP,
            None,
            "bolusDeliveriedTime",  # key
            "Last Bolus Delivered Time",  # name
            TIMELINE_ICON,
            None,
            None,
        ),
        MedtrumEasyViewSensor(
            coordinator,
            DeviceType.PUMP,
            None,
            SensorStateClass.MEASUREMENT,
            "bolusDeliveried",  # key
            "Last Bolus Delivered Volume",  # name
            BOLUS_ICON,
            "U",  # Insulin units
            None,
        ),
        MedtrumEasyViewSensor(
            coordinator,
            DeviceType.PUMP,
            None,
            SensorStateClass.MEASUREMENT,
            "iob",  # key
            "Active Insulin",  # name
            VOLUME_ICON,
            "U",  # Insulin units
            None,
        ),
    ]

    async_add_entities(sensors)


class MedtrumEasyViewSensor(MedtrumEasyViewDevice, SensorEntity):
    """MedtrumEasyView Sensor class."""

    def __init__(  # noqa: PLR0913
        self,
        coordinator: MedtrumEasyViewDataUpdateCoordinator,
        device_type: DeviceType,
        device_class: SensorDeviceClass | None,
        state_class: SensorStateClass | None,
        key: str,
        name: str,
        icon: str | None,
        unit_of_measurement: str | None,
        suggested_unit_of_measurement: str | None,
    ) -> None:
        """Initialize the device class."""
        super().__init__(coordinator)
        self.uom = unit_of_measurement
        self._attr_unique_id = (
            f"{self.coordinator.data['uid']}_{device_type.value}_{key}"
        )
        self._attr_name = name
        self.key = key
        self._icon = icon
        self.device_type = device_type

        # set parent class attributes
        self._attr_device_class = device_class
        self._attr_state_class = state_class
        self._attr_suggested_unit_of_measurement = suggested_unit_of_measurement
        self._attr_suggested_display_precision = 2

    @property
    def native_value(self) -> Any:
        """Return the native value of the sensor."""
        if self.coordinator.data is not None:
            value = self.coordinator.data[self.device_type.value + "_status"][self.key]

            # Convert timestamp to datetime for TIMESTAMP device class
            if (
                self._attr_device_class == SensorDeviceClass.TIMESTAMP
                and value is not None
            ):
                return datetime.fromtimestamp(value, tz=UTC)

            # Convert pump status integer to string for ENUM device class
            if (
                self._attr_device_class == SensorDeviceClass.ENUM
                and self.key == "status"
                and value is not None
            ):
                try:
                    return PumpStatus(value).name.replace("_", " ").title()
                except ValueError:
                    return f"Unknown Status ({value})"

            return value

        return None

    @property
    def icon(self) -> str | None:
        """Return the icon for the frontend."""
        if self._icon:
            return self._icon

        # Pump sensors
        if self.device_type == DeviceType.PUMP:
            return PUMP_ICON

        # Sensor sensors
        if self.device_type == DeviceType.SENSOR:
            return SENSOR_ICON

        return None

    @property
    def native_unit_of_measurement(self) -> str | None:
        """Return the native unit of measurement."""
        return self.uom
