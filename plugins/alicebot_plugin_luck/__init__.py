import re
import time
import random

from plugins.alicebot_plugin_base import CommandPluginBase

from .config import Config


class Luck(CommandPluginBase[None, Config]):
    plugin_config_class: Config = Config

    def __post_init__(self):
        self.re_pattern = re.compile(r".*", flags=re.I)

    async def handle(self) -> None:
        random.seed(
            time.strftime("%Y%j", time.localtime()) + self.format_str("{user_id}")
        )
        lucy = random.randint(self.plugin_config.min_int, self.plugin_config.max_int)
        await self.event.reply(
            self.format_str(self.plugin_config.message_str, str(lucy))
        )
