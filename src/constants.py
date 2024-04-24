from __future__ import annotations

import datetime as dt
import os
import sys as s
from itertools import cycle
from typing import TYPE_CHECKING, Any, Iterable, Mapping

import disnake
from disnake import __version__ as disnake_version
from tabulate import tabulate

from src import __version__ as bot_version
from src import log

if TYPE_CHECKING:
    from disnake import Permissions

logger = log.get_logger(__name__)

try:
    import dotenv
except ModuleNotFoundError:
    pass
else:
    if dotenv.find_dotenv():
        logger.info("Found .env file, loading environment variables")

        dotenv.load_dotenv(override=True)

ASCII_TEXT_ART = r"""

  ____        _     _______                   _       _
 |  _ \      | |   |__   __|                 | |     | |
 | |_) | ___ | |_     | | ___ _ __ ___  _ __ | | __ _| |_ ___
 |  _ < / _ \| __|    | |/ _ \ '_ ` _ \| '_ \| |/ _` | __/ _ \
 | |_) | (_) | |_     | |  __/ | | | | | |_) | | (_| | ||  __/
 |____/ \___/ \__|    |_|\___|_| |_| |_| .__/|_|\__,_|\__\___|
                                       | |
                                       |_|

"""
# https://patorjk.com/software/taag/#p=display&f=Big


class Client:
    """Bot config."""

    owner_ids: tuple[int, ...] = ()  # User: { username }

    activities = cycle(["/help"])
    activity_type = disnake.ActivityType.watching
    activity_status = disnake.Status.online

    support_server_id: int = 900741649074896906
    support_server_code: str = "example"
    support_server = "https://example.com"

    token: str | None = os.getenv("TOKEN")

    reload = True

    admin_permissions: Permissions = disnake.Permissions(administrator=True)
    standard_permissions: Permissions = disnake.Permissions(
        change_nickname=True,
        create_instant_invite=True,
        read_messages=True,
        view_channel=True,
        add_reactions=True,
        attach_files=True,
        embed_links=True,
        read_message_history=True,
        send_messages=True,
        send_messages_in_threads=True,
        use_external_emojis=True,
        connect=True,
        speak=True,
    )


class Color:
    """Colors used in various embeds."""

    RED = disnake.Color.red()
    BLUE = disnake.Color.blue()
    BLURPLE = disnake.Color.blurple()
    ORANGE = disnake.Color.orange()
    GREY = disnake.Color.darker_grey()
    LIGHT_GREY = disnake.Color.light_grey()
    TEAL = disnake.Color.teal()
    PURPLE = disnake.Color.purple()
    GREEN = disnake.Color.green()


class Emoji:
    """Contain emojis used within the bot."""

    uptime: str = "🟢"
    version: str = "#️⃣"
    ping: str = "⌛"
    owners: str = "👑"
    support: str = "🆘"
    resources: str = "🗒️"
    members: str = "🙋"
    trashcan: str = "🗑️"


def generate_table(data: Mapping[str, Iterable[Any]] | Iterable[Iterable[Any]]) -> str:
    """Generate a rounded table with tabulate."""
    return tabulate(data, tablefmt="rounded_outline")


def generate_startup_table(bot_name: str, bot_id: int) -> str:
    """Generate the table for startup."""
    now = dt.datetime.now(tz=dt.timezone.utc)

    return generate_table(
        data=[
            ["Started", now.strftime("%m/%d/%Y - %H:%M:%S")],
            ["System Version", s.version],
            ["Disnake Version", disnake_version],
            ["Bot Version", bot_version],
            ["Connected as", f"{bot_name} ({bot_id})"],
        ],
    )
