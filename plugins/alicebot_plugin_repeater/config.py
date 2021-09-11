from plugins.alicebot_plugin_public import Config as BaseConfig


class Config(BaseConfig):
    __config_name__ = 'plugin_repeater'
    get_timeout: int = 100
    """get() 方法的 timeout 参数。"""
