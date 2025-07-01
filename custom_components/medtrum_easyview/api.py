"""Provide a Medtrum EasyView API client."""

from __future__ import annotations

import asyncio
import base64
import json
import logging
import socket
from datetime import UTC, datetime
from typing import (
    Any,
)

import aiohttp

from .const import (
    API_TIME_OUT_SECONDS,
    APP_TAG,
    CONTENT_TYPE,
    LOGIN_URL,
    STATUS_URL,
)

_LOGGER = logging.getLogger(__name__)


class MedtrumEasyViewApiClient:
    """
    API class to retrieve medtrum easyview data.

    Attributes:
        username: of the medtrum easyview account
        password: of the medtrum easyview account
        base_url: For API calls depending on your location
        Session: aiottp object for the open session

    """

    def __init__(
        self,
        username: str,
        password: str,
        base_url: str,
        session: aiohttp.ClientSession,
    ) -> None:
        """Sample API Client."""
        self._username = username
        self._password = password
        self.login_url = base_url + LOGIN_URL
        self.status_url = base_url + STATUS_URL
        self._session = session

    async def async_login(self) -> Any:
        """Get token from the API."""
        response_login = await api_wrapper(
            self._session,
            method="post",
            url=self.login_url,
            headers={
                "AppTag": APP_TAG,
                "Accept": CONTENT_TYPE,
                "Content-Type": CONTENT_TYPE,
            },
            data={
                "user_name": self._username,
                "password": self._password,
                "user_type": "P",
            },
        )
        _LOGGER.debug(
            "Login status : %s",
            response_login,
        )
        if response_login["error"] != 0:
            raise MedtrumEasyViewApiAuthenticationError(  # noqa: TRY003
                "Invalid credentials",  # noqa: EM101
            )

        self.uid = str(int(response_login["uid"]))
        self.realname = response_login["realname"]

        return self.uid

    async def async_get_data(self) -> Any:
        """Get data from the API."""
        # Create param with base64 encoded timestamp data for current day
        now = datetime.now(UTC)
        start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = start_of_day.replace(
            hour=23, minute=59, second=59, microsecond=999999
        )

        param_data = {
            "ts": [int(start_of_day.timestamp()), int(end_of_day.timestamp())],
            "tz": 0,  # UTC+0
        }
        param_encoded = base64.b64encode(json.dumps(param_data).encode()).decode()

        url = self.status_url.replace("$userid", self.uid) + f"?param={param_encoded}"

        response = await api_wrapper(
            self._session,
            method="get",
            url=url,
            headers={
                "AppTag": APP_TAG,
                "Accept": CONTENT_TYPE,
                "Content-Type": CONTENT_TYPE,
            },
            data={},
        )

        # handle cookie expiration

        _LOGGER.debug(
            "Return API Status: %s",
            response,
        )

        # API status return 0 if everything goes well.
        # if response["error"] == 0:
        data = response["data"]

        # Add uid, realname to the data for later use.
        data["uid"] = self.uid
        data["realname"] = self.realname

        _LOGGER.debug(
            "Raw data: %s",
            data,
        )

        return data


################################################################
#            """Utilitises """               #
################################################################


@staticmethod
async def api_wrapper(
    session: aiohttp.ClientSession,
    method: str,
    url: str,
    data: dict | None = None,
    headers: dict | None = None,
) -> Any:
    """Get information from the API."""
    try:
        async with asyncio.timeout(API_TIME_OUT_SECONDS):
            response = await session.request(
                method=method,
                url=url,
                headers=headers,
                json=data,
            )
            _LOGGER.debug("response.status: %s", response.status)
            if response.status in (401, 403):
                raise MedtrumEasyViewApiAuthenticationError(  # noqa:TRY003,TRY301
                    "Invalid credentials",  # noqa: EM101
                )
            response.raise_for_status()
            return await response.json()

    except TimeoutError as exception:
        raise MedtrumEasyViewCommunicationError(  # noqa: TRY003
            "Timeout error fetching information",  # noqa: EM101
        ) from exception
    except (aiohttp.ClientError, socket.gaierror) as exception:
        raise MedtrumEasyViewCommunicationError(  # noqa: TRY003
            "Error fetching information",  # noqa: EM101
        ) from exception
    except Exception as exception:  # pylint: disable=broad-except
        raise MedtrumEasyViewApiError("Something really wrong happened!") from exception  # noqa: TRY003,EM101


class MedtrumEasyViewApiError(Exception):
    """Exception to indicate a general API error."""

    _LOGGER.debug("Exception: general API error")


class MedtrumEasyViewCommunicationError(MedtrumEasyViewApiError):
    """Exception to indicate a communication error."""

    _LOGGER.debug("Exception: communication error")


class MedtrumEasyViewApiAuthenticationError(MedtrumEasyViewApiError):
    """Exception to indicate an authentication error."""

    _LOGGER.debug("Exception: authentication error")
