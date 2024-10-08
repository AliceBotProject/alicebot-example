from pydantic import Field

from plugins.alicebot_plugin_base import CommandPluginConfig


class Config(CommandPluginConfig):
    __config_name__ = "plugin_echo"
    command: set[str] = Field(default_factory=lambda: {"echo"})
    """命令文本。"""
    message_str: str = "复读{user_name}: {message}"
    """最终发送消息的格式。"""
