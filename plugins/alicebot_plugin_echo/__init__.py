import re
from typing import Any

from alicebot import MessageEvent

from plugins.alicebot_plugin_base import CommandPluginBase

from .config import Config


class Echo(CommandPluginBase[MessageEvent[Any], None, Config]):
    command_re_pattern = re.compile(r"(?P<echo_str>.*)", flags=re.IGNORECASE)

    async def handle(self) -> None:
        await self.event.reply(
            self.format_str(
                self.config.message_str, self.command_match.group("echo_str")
            )
        )
