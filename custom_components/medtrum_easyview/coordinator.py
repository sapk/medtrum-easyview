"""DataUpdateCoordinator for Medtrum EasyView."""

from __future__ import annotations

from datetime import timedelta
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import MedtrumEasyViewApiAuthenticationError, MedtrumEasyViewApiClient, MedtrumEasyViewApiError
from .const import DOMAIN, LOGGER, REFRESH_RATE_MIN

_LOGGER = logging.getLogger(__name__)


class MedtrumEasyViewDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the API. single endpoint."""

    config_entry: ConfigEntry

    def __init__(
        self,
        hass: HomeAssistant,
        client: MedtrumEasyViewApiClient,
    ) -> None:
        """Initialize."""
        self.client = client

        super().__init__(
            hass=hass,
            logger=LOGGER,
            name=DOMAIN,
            update_interval=timedelta(minutes=REFRESH_RATE_MIN),
        )

    async def _async_update_data(self):
        """Update data via library."""
        try:
            return await self.client.async_get_data()
        except MedtrumEasyViewApiAuthenticationError as exception:
            _LOGGER.debug("Exception: authentication error during coordinator update")
            raise ConfigEntryAuthFailed(exception) from exception
        except MedtrumEasyViewApiError as exception:
            _LOGGER.debug("Exception: general API error during coordinator update")
            raise UpdateFailed(exception) from exception
