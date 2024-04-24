from __future__ import annotations

import disnake

from src.constants import Client, Emoji


class SupportInvite(disnake.ui.Button[None]):
    """A button that will invite the interacting member to the support server.

    This button uses low-level component listeners (@bot.listen('on_button_click')
    """

    def __init__(self) -> None:
        super().__init__(
            style=disnake.ButtonStyle.url,
            emoji=Emoji.support,
            url=f"https://discord.gg/{Client.support_server_code}",
        )
