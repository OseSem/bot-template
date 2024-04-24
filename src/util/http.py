from __future__ import annotations

import asyncio
import typing as t

import aiohttp
import yarl

from src import errors, log

logger = log.get_logger(__name__)


SUCCESS_STATUS: int = 200


async def json_or_text(
    response: aiohttp.ClientResponse,
) -> dict[str, t.Any] | list[dict[str, t.Any]] | str:
    """
    Process an `aiohttp.ClientResponse` to return either a JSON object or raw text.

    This function attempts to parse the response as JSON. If the content type of the response is not
    application/json or parsing fails, it falls back to returning the raw text of the response.

    Parameters
    ----------
    response : aiohttp.ClientResponse
        The response object to process.

    Returns
    -------
    dict[str, t.Any] | list[dict[str, t.Any]] | str
        The parsed JSON object as a dictionary or list of dictionaries, or the raw response text.
    """
    try:
        if "application/json" in response.headers["content-type"].lower():
            return await response.json()
    except KeyError:
        # Thanks Cloudflare
        pass

    return await response.text(encoding="utf-8")


class Route:
    """Handle route construction for HTTP requests."""

    def __init__(self, method: str, url: str, **params: int | str | bool) -> None:
        self.method = method

        new_url: yarl.URL = yarl.URL(url).with_query(params)
        self.url: str = new_url.human_repr()


class APIHTTPClient:
    """Represent an HTTP Client used for making requests to APIs."""

    def __init__(
        self,
        connector: aiohttp.BaseConnector | None = None,
        *,
        loop: asyncio.AbstractEventLoop | None = None,
    ) -> None:
        self.loop = loop or asyncio.get_running_loop()
        self.connector = connector

        self.__session: aiohttp.ClientSession = None  # type: ignore[reportAttributeAccessIssue]

        self.ensure_session()

    def ensure_session(self) -> None:
        """
        Ensure that an aiohttp.ClientSession is created and open.

        If a session does not exist or is closed, this method creates a new aiohttp.ClientSession
        using the provided connector and loop.
        """
        if not self.__session or self.__session.closed:
            self.__session = aiohttp.ClientSession(connector=self.connector, loop=self.loop)

    async def request(
        self,
        route: Route,
        headers: dict[str, str] | None = None,
    ) -> dict[str, t.Any] | list[dict[str, t.Any]] | str:
        """
        Send a request to the specified route and returns the response.

        This method constructs and sends an HTTP request based on the specified route and headers.
        It processes the response to return JSON data or raw text, handling errors as needed.

        Parameters
        ----------
        route : Route
            The route object containing the method and URL for the request.
        headers : dict[str, str] | None, optional
            Optional headers to include with the request. Defaults to None.

        Returns
        -------
        dict[str, t.Any] | list[dict[str, t.Any]] | str
            The response data as a parsed JSON object or list, or raw text if JSON parsing is
            not applicable.

        Raises
        ------
        errors.GeneralHTTPError
            Will raise if the request fails or the response indicates an error.
        """
        self.ensure_session()

        method = route.method
        url = route.url

        _headers = {"Accept": "application/json"}

        if headers:
            headers.update(**_headers)
        else:
            headers = _headers

        async with self.__session.request(method, url, headers=headers) as response:
            logger.debug(f"{method} {url} returned {response.status}")

            # errors typically have text involved, so this should be safe 99.5% of the time.
            data = await json_or_text(response)
            logger.debug(f"{method} {url} received {data}")

            if response.status == SUCCESS_STATUS:

                return data

            raise errors.GeneralHTTPError(method, url, response.status)
