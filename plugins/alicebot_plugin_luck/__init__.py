import re
import time
from random import Random
from typing import Any

from alicebot import MessageEvent

from plugins.alicebot_plugin_base import CommandPluginBase

from .config import Config


class Luck(CommandPluginBase[MessageEvent[Any], None, Config]):
    command_re_pattern = re.compile(r".*", flags=re.IGNORECASE)

    async def handle(self) -> None:
        r = Random(
            time.strftime("%Y%j", time.localtime()) + self.format_str("{user_id}")
        )
        await self.event.reply(
            self.format_str(
                self.config.message_str,
                str(r.randint(self.config.min_int, self.config.max_int)),
            )
        )
