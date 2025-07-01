"""Sensor platform for Medtrum EasyView."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)

from .const import (
    DOMAIN,
    GLUCOSE_VALUE_ICON,
    DeviceType,
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

    sensors = [
        MedtrumEasyViewSensor(
            coordinator,
            DeviceType.PUMP,
            SensorDeviceClass.ENUM,
            None,
            "status",  # key
            "Pump Status",  # name
            None,
        ),
        MedtrumEasyViewSensor(
            coordinator,
            DeviceType.PUMP,
            SensorDeviceClass.DURATION,
            SensorStateClass.MEASUREMENT,
            "remainingTime",  # key
            "Pump Remaining time",  # name
            "min",
        ),
        MedtrumEasyViewSensor(
            coordinator,
            DeviceType.PUMP,
            SensorDeviceClass.VOLUME_STORAGE,
            SensorStateClass.MEASUREMENT,
            "remainingDose",  # key
            "Pump Remaining dose",  # name
            "U",
        ),
        MedtrumEasyViewSensor(
            coordinator,
            DeviceType.PUMP,
            SensorDeviceClass.TIMESTAMP,
            None,
            "updateTime",  # key
            "Pump Last update",  # name
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
        device_class: SensorDeviceClass,
        state_class: SensorStateClass | None,
        key: str,
        name: str,
        unit_of_measurement: str | None,
    ) -> None:
        """Initialize the device class."""
        super().__init__(coordinator)
        self.uom = unit_of_measurement
        self._attr_unique_id = (
            f"{self.coordinator.data['uid']}_{self.device_type.value}_{key}"
        )
        self._attr_name = name
        self.key = key
        self.device_type = device_type

        # set parent class attributes
        self._attr_device_class = device_class
        self._attr_state_class = state_class

    @property
    def native_value(self) -> Any:
        """Return the native value of the sensor."""
        if self.coordinator.data is not None:
            return self.coordinator.data[self.device_type.value + "_status"][self.key]

        return None

    @property
    def icon(self) -> str:
        """Return the icon for the frontend."""
        return GLUCOSE_VALUE_ICON

    @property
    def unit_of_measurement(self) -> str | None:
        """Used for glucose measurement and medtrum easyview sensor."""
        return self.uom

    @property
    def extra_state_attributes(self) -> Any:
        """Return the state attributes of the medtrum easyview sensor."""
        if (
            self.coordinator.data
            and self.key == "status"
            and self.coordinator.data[self.device_type.value + "_status"] is not None
        ):
            return {
                "Serial number": hex(
                    self.coordinator.data[self.device_type.value + "_status"]["serial"]
                )[2:].upper(),
                "User ID": self.coordinator.data["uid"],
                "Patient": self.coordinator.data["realname"],
            }

        return None
