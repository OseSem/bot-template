import asyncio
import os
import signal
import sys

import disnake

from src import constants, log
from src.bot import Bot
from src.constants import Client

logger = log.get_logger(__name__)

_intents = disnake.Intents.all()


async def main() -> None:
    """Start bot."""
    bot = Bot(
        intents=_intents,
        owner_ids=set(constants.Client.owner_ids),
        reload=constants.Client.reload,
    )

    bot.i18n.load("src/lang/")  # type: ignore[reportUnknownMemberType]

    try:
        bot.load_extensions("src/exts")
    except Exception:
        await bot.close()
        raise

    logger.info("Bot is starting.")

    try:
        if os.name != "nt":
            # start process for linux host
            loop = asyncio.get_event_loop()

            future = asyncio.ensure_future(bot.start(Client.token or ""), loop=loop)
            loop.add_signal_handler(signal.SIGINT, lambda: future.cancel())
            loop.add_signal_handler(signal.SIGTERM, lambda: future.cancel())

            await future

        else:
            await bot.start(Client.token or "")

    except (asyncio.CancelledError, KeyboardInterrupt):
        logger.warning("Kill command received. Bot is closed.")
        if not bot.is_closed():
            await bot.close()
    except disnake.errors.PrivilegedIntentsRequired:
        msg = f"""Missing Privileged Intents.
        Fix this by adding the required privileged intents for your bot inside of:
        | https://discord.com/developers/applications/{bot.user.id}/bot
        """
        logger.critical(msg)
        if not bot.is_closed():
            await bot.close()


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
