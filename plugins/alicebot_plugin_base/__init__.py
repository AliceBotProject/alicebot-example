import re
from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

from alicebot import MessageEvent, Plugin
from alicebot.typing import StateT

from .config import BasePluginConfig, CommandPluginConfig, RegexPluginConfig

ConfigT = TypeVar("ConfigT", bound=BasePluginConfig)
RegexPluginConfigT = TypeVar("RegexPluginConfigT", bound=RegexPluginConfig)
CommandPluginConfigT = TypeVar("CommandPluginConfigT", bound=CommandPluginConfig)
EventT = TypeVar("EventT", bound=MessageEvent[Any])


class BasePlugin(
    Plugin[EventT, StateT, ConfigT],
    ABC,
    Generic[EventT, StateT, ConfigT],
):
    def format_str(self, format_str: str, message_str: str = "") -> str:
        return format_str.format(
            message=message_str,
            user_name=self.get_event_sender_name(),
            user_id=self.get_event_sender_id(),
        )

    def get_event_sender_name(self) -> str:
        from alicebot.adapter.cqhttp.event import MessageEvent as CQHTTPMessageEvent
        from alicebot.adapter.mirai.event import FriendInfo, GroupMemberInfo
        from alicebot.adapter.mirai.event import MessageEvent as MiraiMessageEvent
        from alicebot.adapter.onebot.event import MessageEvent as OneBotMessageEvent

        if isinstance(self.event, CQHTTPMessageEvent):
            return self.event.sender.nickname or ""
        if isinstance(self.event, MiraiMessageEvent):
            if isinstance(self.event.sender, FriendInfo):
                return self.event.sender.nickname
            if isinstance(self.event.sender, GroupMemberInfo):
                return self.event.sender.memberName
        if isinstance(self.event, OneBotMessageEvent):
            return ""
        return ""

    def get_event_sender_id(self) -> str:
        from alicebot.adapter.cqhttp.event import MessageEvent as CQHTTPMessageEvent
        from alicebot.adapter.mirai.event import MessageEvent as MiraiMessageEvent
        from alicebot.adapter.onebot.event import MessageEvent as OneBotMessageEvent

        if isinstance(self.event, CQHTTPMessageEvent):
            if self.event.sender.user_id is not None:
                return str(self.event.sender.user_id)
            return ""
        if isinstance(self.event, MiraiMessageEvent):
            return str(self.event.sender.id)
        if isinstance(self.event, OneBotMessageEvent):
            return str(self.event.user_id)
        return ""

    async def rule(self) -> bool:
        return isinstance(self.event, MessageEvent) and self.str_match(
            self.event.get_plain_text()
        )

    @abstractmethod
    def str_match(self, msg_str: str) -> bool:
        raise NotImplementedError


class RegexPluginBase(BasePlugin[EventT, StateT, RegexPluginConfigT], ABC):
    msg_match: re.Match[str]
    re_pattern: re.Pattern[str]

    def str_match(self, msg_str: str) -> bool:
        msg_str = msg_str.strip()
        msg_match = self.re_pattern.fullmatch(msg_str)
        if msg_match is None:
            return False
        self.msg_match = msg_match
        return bool(self.msg_match)


class CommandPluginBase(RegexPluginBase[EventT, StateT, CommandPluginConfigT], ABC):
    command_match: re.Match[str]
    command_re_pattern: re.Pattern[str]

    def str_match(self, msg_str: str) -> bool:
        if not hasattr(self, "re_pattern"):
            self.re_pattern = re.compile(
                f'[{"".join(self.config.command_prefix)}]'
                f'({"|".join(self.config.command)})'
                r"\s*(?P<command_args>.*)",
                flags=re.IGNORECASE if self.config.ignore_case else 0,
            )
        msg_str = msg_str.strip()
        msg_match = self.re_pattern.fullmatch(msg_str)
        if not msg_match:
            return False
        self.msg_match = msg_match
        command_match = self.re_pattern.fullmatch(self.msg_match.group("command_args"))
        if not command_match:
            return False
        self.command_match = command_match
        return True
