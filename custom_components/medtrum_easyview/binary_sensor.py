"""Binary sensor platform for medtrum easyview."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from homeassistant.components.binary_sensor import BinarySensorEntity

from .const import DOMAIN, DeviceType
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
            key="autobasalStatus",
            name="Basal Active",
        ),
    ]
    async_add_entities(sensors)


class MedtrumEasyViewBinarySensor(MedtrumEasyViewDevice, BinarySensorEntity):
    """medtrum easyview binary_sensor class."""

    def __init__(
        self,
        coordinator: MedtrumEasyViewDataUpdateCoordinator,
        device_type: DeviceType,
        key: str,
        name: str,
    ) -> None:
        """Initialize the device class."""
        super().__init__(coordinator)

        self.key = key
        self._attr_name = name
        self.coordinator = coordinator
        self.device_type = device_type

    # define unique_id based on patient id and sensor key
    @property
    def unique_id(self) -> str:
        """Return a unique id for the sensor."""
        return f"{self.coordinator.data['uid']}_{self.device_type.value}_{self.key}"

    # define state based on the entity_description key
    @property
    def is_on(self) -> bool:
        """Return true if the binary_sensor is on."""
        return True


#        bool(
#            int(self.coordinator.data[self.device_type.value + "_status"][self.key]) > 0
#        )
