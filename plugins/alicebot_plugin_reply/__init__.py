import json
import re
from typing import Any, Dict, Union

from plugins.alicebot_plugin_base import BasePlugin

from .config import Config


class Reply(BasePlugin[None, Config], config=Config):
    priority = 1

    def __init__(self) -> None:
        with self.config.data_file.open() as fp:
            if self.config.data_type == "json":
                json_data = json.load(fp)
            else:
                raise ValueError(f"data_type must be json, not {self.config.data_type}")
        self.rule_to_message: Dict[str, Union[str, Any]] = {
            item["rule"]: item["message"]
            for item in json_data
            if isinstance(item, dict) and "rule" in item and "message" in item
        }

    async def handle(self) -> None:
        msg = self.rule_to_message[self.msg_match.re.pattern]
        if isinstance(msg, str):
            await self.event.reply(self.format_str(msg, self.msg_match.string))
        else:
            await self.event.reply(msg)

    def str_match(self, msg_str: str) -> bool:
        for rule in self.rule_to_message:
            msg_match = re.fullmatch(
                rule,
                msg_str.strip(),
                flags=re.I if self.config.ignore_case else 0,
            )
            if msg_match:
                self.msg_match = msg_match
                return bool(self.msg_match)
        return False
