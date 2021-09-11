from typing import Set

from plugins.alicebot_plugin_public import Config as BaseConfig


class Config(BaseConfig):
    __config_name__ = 'plugin_echo'
    command: Set[str] = {'echo'}
    """命令文本。"""
    message_str: str = '复读{user_name}: {message}'
    """最终发送消息的格式。"""
