from __future__ import annotations

import disnake
from disnake.ext import plugins as p

from src import log
from src.bot import Bot
from src.components import trash

logger = log.get_logger(__name__)

plugin = p.Plugin[Bot]()


@plugin.listener("on_button_click")
async def handle_trash_button(inter: disnake.MessageInteraction) -> None:
    """Handle message deletion when trash button clicked.

    While most of our responses are going to be interaction responses, this button listener
    will allow the use of appending the trash button to non interaction response messages
    like dm messages or regular channel messages sent for other reasons.
    """
    if not inter.component.custom_id or not inter.component.custom_id.startswith(
        trash.TRASH_BUTTON_CUSTOM_ID,
    ):
        return

    custom_id = inter.component.custom_id.removeprefix(trash.TRASH_BUTTON_CUSTOM_ID)
    perms, user_id, *_ = custom_id.split(":")
    perms, user_id = int(perms), int(user_id)

    # check if user is the allowed user OR check if the user has required permissions
    # missing permissions message sent here if user cannot delete.
    if not await has_permission_to_delete(inter, user_id, perms):
        await inter.response.send_message(
            "Sorry. You are not permitted to delete this message.",
            ephemeral=True,
        )
        return

    await inter.response.defer()
    await inter.delete_original_response()


async def has_permission_to_delete(
    inter: disnake.MessageInteraction,
    user_id: int,
    perms: int,
) -> bool:
    """Check if the user has permission to delete the message.

    Parameters
    ----------
    inter : disnake.MessageInteraction
        The interaction to work with

    user_id : int
        The ID of the user you want to check the permissions from.

    perms : int
        The permissions the user has to have.

    Returns
    -------
    bool
        Whether the user has the permission to delete the messages or not.
    """
    if inter.author.id == user_id:
        return True

    permissions = disnake.Permissions(perms)
    user_permissions = inter.permissions

    if permissions.value & user_permissions.value:
        return True

    return False


async def delete_message_without_interaction(msg: disnake.Message | disnake.PartialMessage) -> None:
    """Delete a message not attached to an interaction response.

    Parameters
    ----------
    msg : disnake.Message or disnake.PartialMessage
        The message you want deleted.


    """
    try:
        await msg.delete()
    except disnake.NotFound:
        # message might have already been deleted.
        pass
    except disnake.Forbidden:
        logger.warning("Could not delete message. Cache may be unreliable.")


setup, teardown = plugin.create_extension_handlers()
