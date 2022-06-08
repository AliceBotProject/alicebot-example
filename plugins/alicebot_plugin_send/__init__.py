import re

from plugins.alicebot_plugin_public import BasePlugin

from .config import Config


class Send(BasePlugin[Config]):
    plugin_config_class: Config = Config

    def __post_init__(self):
        self.re_pattern = re.compile(
            f'({"|".join(self.plugin_config.command_prefix | getattr(self.config, "command_prefix", set()))})'
            + f'({"|".join(self.plugin_config.command)})'
            + r"\s*(?P<message>.*)",
            flags=re.I,
        )

    async def handle(self) -> None:
        try:
            await self.send(
                self.msg_match.group("message"),
                "private",
                self.plugin_config.send_user_id,
            )
        except Exception as e:
            if self.plugin_config.send_filed_msg is not None:
                await self.event.reply(
                    self.format_str(self.plugin_config.send_filed_msg, repr(e))
                )
        else:
            if self.plugin_config.send_success_msg is not None:
                await self.event.reply(
                    self.format_str(self.plugin_config.send_success_msg)
                )
