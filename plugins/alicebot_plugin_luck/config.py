from typing import Set

from plugins.alicebot_plugin_public import Config as BaseConfig


class Config(BaseConfig):
    __config_name__ = 'plugin_luck'
    command: Set[str] = {'luck'}
    """命令文本。"""
    min_int: int = 0
    """最小随机整数。"""
    max_int: int = 100
    """最大随机整数。"""
    message_str: str = '{user_name}今天的运气是: {message}'
