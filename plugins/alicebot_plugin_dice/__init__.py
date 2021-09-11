import re
import random

from alicebot.log import logger

from plugins.alicebot_plugin_public import BasePlugin

from .config import Config


class Dice(BasePlugin[Config]):
    plugin_config_class: Config = Config

    def __post_init__(self):
        self.re_pattern = re.compile(
            f'({"|".join(self.plugin_config.command_prefix | getattr(self.config, "command_prefix", set()))})' +
            f'({"|".join(self.plugin_config.command)})' +
            r'\s*(?P<dice_times>[0-9]+)[d](?P<dice_faces>[0-9]+)([*x](?P<dice_multiply>[0-9]+))?.*',
            flags=re.I
        )

    async def handle(self) -> None:
        dice_times = int(self.msg_match.group('dice_times'))
        dice_faces = int(self.msg_match.group('dice_faces'))
        if self.msg_match.group('dice_multiply') is None:
            dice_multiply = None
        else:
            dice_multiply = int(self.msg_match.group('dice_multiply'))

        if dice_times > self.plugin_config.max_dice_times:
            await self.event.reply(self.format_str(self.plugin_config.exceed_max_dice_times_str))
            return

        dice = [random.randint(1, dice_faces) for _ in range(dice_times)]
        dice_sum = sum(dice)
        if dice_multiply is None:
            result_str = f'{dice_times}D{dice_faces}='
            if dice_times != 1:
                result_str += f'{"+".join(map(lambda x: str(x), dice))}='
            result_str += str(dice_sum)
        else:
            result_str = f'{dice_times}D{dice_faces}X{dice_multiply}='
            if dice_times != 1:
                result_str += f'({"+".join(map(lambda x: str(x), dice))})X{dice_multiply}='
            result_str += f'{dice_sum}X{dice_multiply}={dice_sum * dice_multiply}'

        logger.info(f'Dice Plugin: {result_str}')
        await self.event.reply(self.format_str(self.plugin_config.message_str, result_str))
