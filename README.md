# Basic Bot Template

<div style="text-align: center;">

![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/OseSem/bot-template/ci.yml)
![GitHub Issues or Pull Requests](https://img.shields.io/github/issues/OseSem/bot-template)
![GitHub License](https://img.shields.io/github/license/OseSem/bot-template)
![GitHub commit activity](https://img.shields.io/github/commit-activity/w/OseSem/bot-template)

</div>

This is a basic bot template for the [Discord API](https://discord.com/developers/docs/intro) using [disnake](https://docs.disnake.dev).


## Key Features
- Neat packaging control.
- Workflows for linting.
- Basic bot setup.

## Getting Started
1. Clone the template ***[here](https://github.com/new?template_name=bot-template&template_owner=OseSem)***.
2. Changing the license and changing the version and authors in `pyproject.toml` and `src/__init__.py`.
3. Installing the dependencies:
```bash
python3 -m pip install poetry
poetry install
```
4. Create a `.env` file in the root directory and add the following:
```env
TOKEN=YOUR_BOT_TOKEN
```
5. Update version and title in `pyproject.toml` and `src/__init__.py`.
6. Run the bot: (Run `exit` to exit the shell.)
```bash
poetry shell
python main.py
```

## Examples
### Making a plugin:
This template uses [`disnake.ext.plugins`](https://github.com/DisnakeCommunity/disnake-ext-plugins) to nicely split bot's functionality into multiple files. Plugins are conceptually similar to cogs, but offer a simplified interface and don't rely on various hacks that cogs use internally.
```python
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

```

### Using localization:
Our template utilizated disnake's built-in i18n with our own small function that formats them with the arguments provided.
```python
plugin.bot.localization.get(
    "{member}'s money:", # Default message if no language is found.
    inter.locale, # The locale from the user found in the interaction
    "BALANCE_CHECK", # The key to the translated message
    member=member.display_name, # All formatted parameters go here.
),
```
