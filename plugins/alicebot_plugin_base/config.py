from typing import Set

from alicebot import ConfigModel
from pydantic import Field


class BasePluginConfig(ConfigModel):
    message_str: str = "{message}"
    """最终发送消息的格式。"""


class RegexPluginConfig(BasePluginConfig):
    pass


class CommandPluginConfig(RegexPluginConfig):
    command_prefix: Set[str] = Field(default_factory=lambda: {".", "。"})
    """命令前缀。"""
    command: Set[str] = Field(default_factory=set)
    """命令文本。"""
    ignore_case: bool = True
    """忽略大小写。"""
