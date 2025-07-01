"""Sensor platform for Medtrum EasyView."""

from __future__ import annotations

from datetime import datetime
import logging
import time

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_UNIT_OF_MEASUREMENT
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    DOMAIN,
    GLUCOSE_VALUE_ICON,
    MG_DL,
    MMOL_DL_TO_MG_DL,
    MMOL_L,
    DeviceType,
)
from .coordinator import MedtrumEasyViewDataUpdateCoordinator
from .device import MedtrumEasyViewDevice

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
):
    """Set up the sensor platform."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]

    # If custom unit of measurement is selectid it is initialized, otherwise MG/DL is used
    try:
        custom_unit = config_entry.data[CONF_UNIT_OF_MEASUREMENT]
    except KeyError:
        custom_unit = MG_DL

    sensors = [
        # MedtrumEasyViewSensor(
        #     coordinator,
        #     "value",  # key
        #     "Glucose Measurement",  # name
        #     custom_unit,
        # ),
        # MedtrumEasyViewSensor(
        #     coordinator,
        #     "sensor",  # key
        #     "Active Sensor",  # name
        #     "days",  # uom
        # ),
        MedtrumEasyViewSensor(
            coordinator,
            DeviceType.PUMP,
            SensorDeviceClass.ENUM,
            "status",  # key
            "Pump Status",  # name
            None,
        ),
        MedtrumEasyViewSensor(
            coordinator,
            DeviceType.PUMP,
            SensorDeviceClass.DURATION,
            "remainingTime",  # key
            "Pump Remaining time",  # name
            "min",
        ),
        MedtrumEasyViewSensor(
            coordinator,
            DeviceType.PUMP,
            SensorDeviceClass.VOLUME_STORAGE,
            "remainingDose",  # key
            "Pump Remaining dose",  # name
            "U",
        ),
        MedtrumEasyViewSensor(
            coordinator,
            DeviceType.PUMP,
            SensorDeviceClass.TIMESTAMP,
            "updateTime",  # key
            "Pump Last update",  # name
            None,
        ),
    ]

    async_add_entities(sensors)


class MedtrumEasyViewSensor(MedtrumEasyViewDevice, SensorEntity):
    """MedtrumEasyView Sensor class."""

    def __init__(
        self,
        coordinator: MedtrumEasyViewDataUpdateCoordinator,
        type: DeviceType,
        device_class: SensorDeviceClass,
        key: str,
        name: str,
        uom,
    ) -> None:
        """Initialize the device class."""
        super().__init__(coordinator)
        self.uom = uom
        self._attr_unique_id = f"{self.coordinator.data['uid']}_{key}"
        self._attr_name = name
        self.key = key
        self.device_class = device_class
        self.type = type

    @property
    def native_value(self):
        """Return the native value of the sensor."""

        result = None

        if self.coordinator.data is not None:
            return self.coordinator.data[self.type.value + "_status"][self.key]

        return None

    @property
    def icon(self):
        """Return the icon for the frontend."""
        return GLUCOSE_VALUE_ICON

    @property
    def unit_of_measurement(self):
        """Only used for glucose measurement and medtrum easyview sensor delay since update."""

        return self.uom

    @property
    def extra_state_attributes(self):
        """Return the state attributes of the medtrum easyview sensor."""
        result = None
        if self.coordinator.data:
            if self.key == "status":
                if self.coordinator.data[self.type.value + "_status"] is not None:
                    result = {
                        "Serial number": hex(
                            self.coordinator.data[self.type.value + "_status"]["serial"]
                        )[2:].upper(),
                        "User ID": self.coordinator.data["uid"],
                        "Patient": self.coordinator.data["realname"],
                    }

            return result
        return result
