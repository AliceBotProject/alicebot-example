import re
import time
import random

from plugins.alicebot_plugin_public import BasePlugin

from .config import Config


class Luck(BasePlugin[Config]):
    plugin_config_class: Config = Config

    def __post_init__(self):
        self.re_pattern = re.compile(
            f'({"|".join(self.plugin_config.command_prefix | getattr(self.config, "command_prefix", set()))})' +
            f'({"|".join(self.plugin_config.command)})' + r'.*',
            flags=re.I
        )

    async def handle(self) -> None:
        random.seed(time.strftime('%Y%j', time.localtime()) + self.format_str('{user_id}'))
        await self.event.replay(self.format_str(self.plugin_config.message_str,
                                                str(random.randint(self.plugin_config.min_int,
                                                                   self.plugin_config.max_int))))
