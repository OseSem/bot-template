from __future__ import annotations

import datetime as dt
import os

import disnake
from disnake.ext import commands, tasks
from helply import Helply

from src import constants, log
from src.util.http import APIHTTPClient
from src.util.localize import Localization

logger = log.get_logger(__name__)


class Bot(commands.AutoShardedInteractionBot):
    """Base bot instance.

    Parameters
    ----------
    intents : disnake.Intents
        All the intents that the bot will use.
    allowed_mentions : disnake.AllowedMentions
        All the mentions that the bot is allowed to send.
    owner_ids : set[int]
        All the IDs of the owners of this bot.
    reload : bool
        Whether to enable automatic extension reloading on file modification for debugging.
    test_guilds: list[int] | None
        This will set whether the bot will only use specific guilds for testing.
        Do not use this in production!
    """

    def __init__(  # noqa: PLR0913
        self,
        intents: disnake.Intents,
        allowed_mentions: disnake.AllowedMentions | None = None,
        *,
        owner_ids: set[int],
        reload: bool,
        test_guilds: list[int] | None = None,
    ) -> None:
        """We initialize the bot class here."""
        super().__init__(
            intents=intents,
            allowed_mentions=allowed_mentions,
            owner_ids=owner_ids,
            reload=reload,
            test_guilds=test_guilds,
        )

        self.helply = Helply(self)

        self.start_time: dt.datetime = dt.datetime.now(tz=dt.timezone.utc)
        self.localization = Localization(self.i18n)

        self.http_client: APIHTTPClient = APIHTTPClient()

    async def on_connect(self) -> None:
        """Execute when bot is connected to the Discord API."""

    async def on_ready(self) -> None:
        """Execute when bot is ready and cache is populated."""
        msg = constants.generate_startup_table(bot_name=self.user.name, bot_id=self.user.id)
        logger.info(f"\n{msg}")

        self.loop_activities.start()

    @tasks.loop(minutes=5)
    async def loop_activities(self) -> None:
        """Loop between activities."""
        if constants.Client.activities:
            await self.change_presence(
                activity=disnake.Activity(
                    name=next(iter(constants.Client.activities)),
                    type=constants.Client.activity_type,
                ),
                status=constants.Client.activity_status,
            )
        else:
            logger.warning("There are no activities provided.")
            await self.change_presence(activity=None, status=constants.Client.activity_status)
            self.loop_activities.stop()

    def load_extensions(self, path: str) -> None:
        """Load all bot extensions.

        Parameters
        ----------
        path: str
            The path where the extensions are found.
        """
        for item in os.listdir(path):
            if "__" in item or not item.endswith(".py"):
                continue

            ext = f"src.exts.{item[:-3]}"
            try:
                super().load_extension(ext)
                logger.info(f"Extension loaded: {item}")
            except commands.errors.NoEntryPointError as e:  # Setup function not found
                logger.critical(f"{e.name} has no setup function.")

    async def get_or_fetch_owners(self) -> list[disnake.User]:
        """Get owners from cache, or fetch them and cache."""
        return [
            owner
            for owner_id in constants.Client.owner_ids
            if (owner := await self.get_or_fetch_user(owner_id))
        ]
