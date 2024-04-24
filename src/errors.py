from src import log

logger = log.get_logger(__name__)

__all__ = (
    "BaseBotError",
    "GeneralHTTPError",
)


class BaseBotError(Exception):
    """Base bot error all custom errors inherit from."""


class GeneralHTTPError(Exception):
    """General HTTP error."""

    def __init__(self, method: str, url: str, status: int) -> None:
        msg = f"{method} request to {url} failed - {status}"
        logger.error(msg)

        super().__init__(f"Request to {url} failed - {status}")
        self.status = status
