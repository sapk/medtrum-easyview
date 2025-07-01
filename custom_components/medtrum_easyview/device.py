"""Sensor platform for Medtrum EasyView."""
from __future__ import annotations

from homeassistant.helpers.device_registry import DeviceInfo

from .const import ATTRIBUTION, DOMAIN, NAME, VERSION
from .coordinator import MedtrumEasyViewDataUpdateCoordinator

from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .coordinator import MedtrumEasyViewDataUpdateCoordinator

import logging

# enable logging
_LOGGER = logging.getLogger(__name__)


# This class is called when a device is created.
# A device is created for each patient to regroup patient entities

class MedtrumEasyViewDevice(CoordinatorEntity):
    """MedtrumEasyViewEntity class."""

    _attr_has_entity_name = True
    _attr_attribution = ATTRIBUTION

    def __init__(
        self,
        coordinator: MedtrumEasyViewDataUpdateCoordinator,
    ) -> None:
        """Initialize."""
        super().__init__(coordinator)

        # Creating unique IDs using for the device based on the medtrum easyview user_id.
        self._attr_unique_id = self.coordinator.data["user_id"]

        _LOGGER.debug(
            "entity unique id is %s",
            self._attr_unique_id,
        )
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self.coordinator.data["user_id"])},
            name=self.coordinator.data["realname"],
            model=VERSION,
            manufacturer=NAME,
            # config_entries=self.coordinator.config_entry,
            # entry_type=DeviceEntryType.SERVICE,
        )
