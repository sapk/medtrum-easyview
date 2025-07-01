"""Custom integration to integrate Medtrum EasyView with Home Assistant."""

from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME, Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import MedtrumEasyViewApiClient
from .const import BASE_URL_LIST, COUNTRY, DOMAIN
from .coordinator import MedtrumEasyViewDataUpdateCoordinator

PLATFORMS: list[Platform] = [
    Platform.SENSOR,
    Platform.BINARY_SENSOR,
]


_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up this integration using UI."""

    _LOGGER.debug(
        "Appel de async_setup_entry entry: entry_id= %s, data= %s, user = %s BaseUrl = %s",
        entry.entry_id,
        entry.data,
        entry.data[CONF_USERNAME],
        #        entry.data[CONF_PASSWORD],
        BASE_URL_LIST.get(entry.data[COUNTRY]),
    )
    hass.data.setdefault(DOMAIN, {})

    #    Using the declared API for login based on patient credentials to retreive the bearer Token

    myMedtrumEasyViewLogin = MedtrumEasyViewApiClient(
        username=entry.data[CONF_USERNAME],
        password=entry.data[CONF_PASSWORD],
        base_url=BASE_URL_LIST.get(entry.data[COUNTRY]) or BASE_URL_LIST["Global"],
        session=async_get_clientsession(hass),
    )

    # Validate credentials
    await myMedtrumEasyViewLogin.async_login()


    hass.data[DOMAIN][entry.entry_id] = coordinator = MedtrumEasyViewDataUpdateCoordinator(
        hass=hass,
        client=myMedtrumEasyViewLogin,
    )

    # First poll of the data to be ready for entities initialization
    await coordinator.async_config_entry_first_refresh()

    # Then launch async_setup_entry for our declared entities in sensor.py and binary_sensor.py
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    # Reload entry when its updated.
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Handle removal of an entry."""
    if unloaded := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)
    return unloaded


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry  when it changed."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
