from pydantic import Field

from plugins.alicebot_plugin_base import CommandPluginConfig


class Config(CommandPluginConfig):
    __config_name__ = "plugin_dice"
    command: set[str] = Field(default_factory=lambda: {"r", "roll", "dice"})
    """命令文本。"""
    max_dice_times: int = 1000
    """最大单次投掷次数。"""
    exceed_max_dice_times_str: str = "错误：超过最大投掷次数。"
    """超过最大单次投掷次数时的提示语。"""
