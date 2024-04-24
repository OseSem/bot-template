from __future__ import annotations

import typing as t

import disnake
from disnake.ext import plugins as p
from helply import utils

from src import log
from src.bot import Bot
from src.components import trash
from src.constants import Color

logger = log.get_logger(__name__)

plugin = p.Plugin[Bot]()

NO_COMMAND = "No commands available."


@plugin.slash_command(name="help")
async def help_command(inter: disnake.CommandInteraction, command: str | None = None) -> None:
    """View bot's commands and their details [USAGE: /help {command}].

    Parameters
    ----------
    command: Select a command to view its details.
    """
    await inter.response.defer()

    if command:
        if command == NO_COMMAND:
            await inter.delete_original_response()
            await inter.followup.send(NO_COMMAND, ephemeral=True)
            return

        command_ = plugin.bot.helply.get_command_named(command, locale=inter.locale)
        if not command_:
            await inter.delete_original_response()
            await inter.followup.send(
                f"Unable to find a command you're permitted to use with the name **{command}**.",
                ephemeral=True,
            )
            return
        embed = utils.command_detail_embed(command_, color=Color.BLURPLE)
        await inter.edit_original_response(
            embed=embed,
            components=[trash.TrashButton(inter.author.id)],
        )
        return

    if inter.guild:
        inter = t.cast(disnake.GuildCommandInteraction, inter)
        await handle_guild_context(inter)
        return

    await handle_dm_context(inter)


@help_command.autocomplete("command")  # type: ignore[reportUnknownMemberType]
async def help_command_autocomplete(inter: disnake.CommandInteraction, string: str) -> list[str]:
    """Autocomplete handler for help command."""
    if inter.guild:
        inter = t.cast(disnake.GuildCommandInteraction, inter)
        commands = plugin.bot.helply.get_guild_commands(
            inter.guild.id,
            permissions=inter.author.guild_permissions,
            locale=inter.locale,
        )
    else:
        commands = plugin.bot.helply.get_dm_only_commands(locale=inter.locale)

    if not commands:
        return [NO_COMMAND]

    return [c.name for c in commands if string.casefold() in c.name.casefold()]


async def handle_guild_context(inter: disnake.GuildCommandInteraction) -> None:
    """Handle helply when called from a guild.

    Parameters
    ----------
    inter : disnake.GuildCommandInteraction |
        The interaction corrosponding to the help command.
    """
    commands = plugin.bot.helply.get_guild_commands(
        inter.guild.id,
        locale=inter.locale,
        permissions=inter.author.guild_permissions,
    )
    if not commands:
        await inter.delete_original_response()
        await inter.followup.send(
            "Unable to find any commands you're permitted to use.",
            ephemeral=True,
        )
        return

    embeds = utils.commands_overview_embeds(
        commands,
        max_field_chars=700,
        max_fields=1,
        color=Color.BLURPLE,
    )
    view = utils.Paginator(embeds=embeds) if len(embeds) > 1 else disnake.utils.MISSING
    trash_button = trash.TrashButton(inter.author.id)
    if view:
        view.add_item(trash_button)  # type: ignore[reportUnknownMemberType]
        components = disnake.utils.MISSING
    else:
        components = [trash_button]

    await inter.edit_original_response(embed=embeds[0], view=view, components=components)
    view.message = await inter.original_response()


async def handle_dm_context(inter: disnake.CommandInteraction) -> None:
    """Handle helply when called from direct message.

    Parameters
    ----------
    inter : disnake.GuildCommandInteraction |
        The interaction corrosponding to the help command.
    """
    commands = plugin.bot.helply.get_dm_only_commands(locale=inter.locale)

    if not commands:
        await inter.edit_original_response(
            "Unable to find any commands you're permitted to use outside of a guild.",
        )
        return

    embeds = utils.commands_overview_embeds(
        commands,
        max_field_chars=700,
        max_fields=1,
        color=Color.BLURPLE,
    )
    view = utils.Paginator(embeds=embeds) if len(embeds) > 1 else disnake.utils.MISSING
    trash_button = trash.TrashButton(inter.author.id)
    if view:
        view.add_item(trash_button)  # type: ignore[reportUnknownMemberType]
        components = disnake.utils.MISSING
    else:
        components = [trash_button]

    await inter.edit_original_response(embed=embeds[0], view=view, components=components)
    view.message = await inter.original_response()


setup, teardown = plugin.create_extension_handlers()
