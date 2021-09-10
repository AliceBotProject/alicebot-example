import re
from abc import ABC
from typing import Generic, TypeVar

from alicebot.plugin import Plugin

from .config import Config

T_Config = TypeVar('T_Config', bound=Config)


class BasePlugin(Plugin, ABC, Generic[T_Config]):
    msg_match: re.Match
    re_pattern: re.Pattern
    plugin_config_class: T_Config = Config

    @property
    def plugin_config(self) -> T_Config:
        return getattr(self.config, self.plugin_config_class.__config_name__)

    def format_str(self, format_str: str, message_str: str = '') -> str:
        if self.adapter.name == 'cqhttp':
            format_str = format_str.format(message=message_str, user_name=self.event.sender.nickname)
        elif self.adapter.name == 'mirai':
            if self.event.type == 'FriendMessage':
                format_str = format_str.format(message=message_str, user_name=self.event.sender.nickname)
            elif self.event.type == 'GroupMessage':
                format_str = format_str.format(message=message_str, user_name=self.event.sender.memberName)
        return format_str

    async def rule(self) -> bool:
        if self.adapter.name == 'cqhttp':
            if self.event.type == 'message':
                if self.plugin_config.handle_all_message:
                    return self.str_match(self.event.message.get_plain_text())
                elif self.event.message_type == 'private' and self.plugin_config.handle_friend_message:
                    return self.str_match(self.event.message.get_plain_text())
                elif self.event.message_type == 'group' and self.plugin_config.handle_group_message:
                    if self.plugin_config.accept_group is None or self.event.group_id in self.plugin_config.accept_group:
                        return self.str_match(self.event.message.get_plain_text())
        elif self.adapter.name == 'mirai':
            if self.plugin_config.handle_all_message:
                return self.str_match(self.event.message.get_plain_text())
            elif self.event.type == 'FriendMessage' and self.plugin_config.handle_friend_message:
                return self.str_match(self.event.message.get_plain_text())
            elif self.event.type == 'GroupMessage' and self.plugin_config.handle_group_message:
                if self.plugin_config.accept_group is None or self.event.sender.group.id in self.plugin_config.accept_group:
                    return self.str_match(self.event.message.get_plain_text())
        return False

    def str_match(self, msg_str: str) -> bool:
        msg_str = msg_str.strip()
        self.msg_match = self.re_pattern.fullmatch(msg_str)
        return bool(self.msg_match)
