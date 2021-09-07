from typing import Set, Optional

from pydantic import BaseModel


class Config(BaseModel):
    __config_name__ = 'plugin-dice'
    command_prefix: Set[str] = {'.', '。'}
    """命令前缀。"""
    command: Set[str] = {'r', 'roll', 'dice'}
    """命令文本。"""
    handle_all_message: bool = False
    """是否处理所有类型的消息，此配置为 True 时会覆盖 handle_friend_message 和 handle_group_message。"""
    handle_friend_message: bool = True
    """是否处理好友消息。"""
    handle_group_message: bool = True
    """是否处理群消息。"""
    accept_group: Optional[Set[int]] = None
    """处理消息的群号，仅当 handle_group_message 为 True 时生效，留空表示处理所有群。"""
    str_prefix: str = '{user_name}: '
    """最终发送消息的前缀。"""
    str_suffix: str = ''
    """最终发送消息的后缀。"""
    max_dice_times: int = 1000
    """最大单次投掷次数。"""
    exceed_max_dice_times_srt: str = '错误：超过最大投掷次数。'
    """超过最大单次投掷次数时的提示语。"""
