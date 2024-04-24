from __future__ import annotations

import disnake

from src.constants import Emoji

TRASH_BUTTON_CUSTOM_ID = "TRASH:"


class TrashButton(disnake.ui.Button[None]):
    """A button that will delete the message when clicked.

    This button uses low-level component listeners (@bot.listen('on_button_click')
    """

    def __init__(  # noqa: PLR0913
        self,
        user: int | disnake.User | disnake.Member,
        *,
        allow_manage_messages: bool = True,
        initial_message: int | disnake.Message | None = None,
        style: disnake.ButtonStyle | None = None,
        emoji: disnake.Emoji | disnake.PartialEmoji | str | None = None,
    ) -> None:
        super().__init__()

        self.custom_id = TRASH_BUTTON_CUSTOM_ID

        user_id = user.id if isinstance(user, (disnake.User | disnake.Member)) else user

        permissions = disnake.Permissions()
        if allow_manage_messages:
            permissions.manage_messages = True

        self.custom_id += f"{permissions.value}:"
        self.custom_id += str(user_id)

        if initial_message:
            if isinstance(initial_message, (disnake.Message | disnake.InteractionMessage)):
                initial_message = initial_message.id

            self.custom_id += f":{initial_message}"

        if style is None:
            if initial_message:
                self.style = disnake.ButtonStyle.danger
            else:
                self.style = disnake.ButtonStyle.secondary
        else:
            self.style = style

        # use trashcan as default
        self.emoji = emoji or Emoji.trashcan
