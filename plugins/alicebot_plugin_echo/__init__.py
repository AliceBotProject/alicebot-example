import re

from plugins.alicebot_plugin_public import BasePlugin

from .config import Config


class Echo(BasePlugin[Config]):
    plugin_config_class: Config = Config

    def __post_init__(self):
        self.re_pattern = re.compile(
            f'({"|".join(self.plugin_config.command_prefix | getattr(self.config, "command_prefix", set()))})' +
            f'({"|".join(self.plugin_config.command)})' + r'(?P<echo_str>.*)',
            flags=re.I
        )

    async def handle(self) -> None:
        await self.event.reply(self.format_str(self.plugin_config.message_str, self.msg_match.group('echo_str')))
