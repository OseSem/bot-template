import disnake
from disnake.ext import plugins as p

from src.bot import Bot

plugin = p.Plugin[Bot]()


@plugin.slash_command()
async def example(_: disnake.CommandInteraction) -> None:
    """Parent Interaction Example."""


@example.sub_command(name="ping")
async def example_ping(inter: disnake.CommandInteraction) -> None:
    """Ping, Pong! [USAGE: /example ping]."""
    await inter.response.send_message("Pong!")


setup, teardown = plugin.create_extension_handlers()
