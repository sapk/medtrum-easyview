"""Binary sensor platform for medtrum easyview."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)

from .const import (
    DOMAIN,
    PUMP_ICON,
    PUMP_OFF_ICON,
    PUMP_ON_ICON,
    SENSOR_ICON,
    DeviceType,
)
from .device import MedtrumEasyViewDevice

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .coordinator import MedtrumEasyViewDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the binary_sensor platform."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]

    sensors = [
        MedtrumEasyViewBinarySensor(
            coordinator,
            device_type=DeviceType.PUMP,
            device_class=BinarySensorDeviceClass.POWER,
            key="autobasalstatus",
            name="Basal Active",
        ),
        MedtrumEasyViewBinarySensor(
            coordinator,
            device_type=DeviceType.PUMP,
            device_class=BinarySensorDeviceClass.CONNECTIVITY,
            key="status",
            name="Pump",
        ),
        MedtrumEasyViewBinarySensor(
            coordinator,
            device_type=DeviceType.SENSOR,
            device_class=BinarySensorDeviceClass.CONNECTIVITY,
            key="status",
            name="Sensor",
        ),
    ]
    async_add_entities(sensors)


class MedtrumEasyViewBinarySensor(MedtrumEasyViewDevice, BinarySensorEntity):
    """medtrum easyview binary_sensor class."""

    def __init__(
        self,
        coordinator: MedtrumEasyViewDataUpdateCoordinator,
        device_type: DeviceType,
        device_class: BinarySensorDeviceClass | None,
        key: str,
        name: str,
    ) -> None:
        """Initialize the device class."""
        super().__init__(coordinator)

        self.key = key
        self._attr_name = name
        self.coordinator = coordinator
        self.device_type = device_type
        self._attr_device_class = device_class

    # define unique_id based on patient id and sensor key
    @property
    def unique_id(self) -> str:
        """Return a unique id for the sensor."""
        return f"{self.coordinator.data['uid']}_{self.device_type.value}_{self.key}"

    @property
    def icon(self) -> str | None:
        """Return the icon for the frontend."""
        if self.device_type == DeviceType.PUMP:
            if self.key == "autobasalstatus":
                return PUMP_ON_ICON if self.is_on else PUMP_OFF_ICON
            return PUMP_ICON
        if self.device_type == DeviceType.SENSOR:
            return SENSOR_ICON

        return None

    # define state based on the entity_description key
    @property
    def is_on(self) -> bool:
        """Return true if the binary_sensor is on."""
        # If the key is not found, return False
        try:
            return (
                int(self.coordinator.data[self.device_type.value + "_status"][self.key])
                > 0
            )
        except KeyError:
            return False
