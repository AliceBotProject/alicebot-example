import re
import random
from alicebot.log import logger
from alicebot.plugin import Plugin

from .config import Config


class Dice(Plugin):
    msg_match: re.Match

    def __post_init__(self):
        self.re_pattern = re.compile(
            f'[{"".join(self.dice_config.command_prefix | getattr(self.config, "command_prefix", set()))}]' +
            f'[{"".join(self.dice_config.command)}]' +
            r'(?P<dice_times>[0-9]+)[d](?P<dice_faces>[0-9]+)([*x](?P<dice_multiply>[0-9]+))?',
            flags=re.I
        )

    @property
    def dice_config(self) -> Config:
        return getattr(self.config, Config.__config_name__)

    async def handle(self) -> None:
        dice_times = int(self.msg_match.group('dice_times'))
        dice_faces = int(self.msg_match.group('dice_faces'))
        if self.msg_match.group('dice_multiply') is None:
            dice_multiply = None
        else:
            dice_multiply = int(self.msg_match.group('dice_multiply'))

        if dice_times > self.dice_config.max_dice_times:
            await self.event.replay(self.format_str(self.dice_config.exceed_max_dice_times_str))
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
        await self.event.replay(self.format_str(self.dice_config.str_prefix) +
                                result_str +
                                self.format_str(self.dice_config.str_suffix))

    def format_str(self, fix_str: str) -> str:
        if self.adapter.name == 'cqhttp':
            return fix_str.format(user_name=self.event.sender.nickname)
        elif self.adapter.name == 'mirai':
            if self.event.type == 'FriendMessage':
                return fix_str.format(user_name=self.event.sender.nickname)
            elif self.event.type == 'GroupMessage':
                return fix_str.format(user_name=self.event.sender.memberName)
        return fix_str

    async def rule(self) -> bool:
        if self.adapter.name == 'cqhttp':
            if self.event.type == 'message':
                if self.dice_config.handle_all_message:
                    return self.str_match(self.event.message.get_plain_text())
                elif self.event.message_type == 'private' and self.dice_config.handle_friend_message:
                    return self.str_match(self.event.message.get_plain_text())
                elif self.event.message_type == 'group' and self.dice_config.handle_group_message:
                    if self.dice_config.accept_group is None or self.event.group_id in self.dice_config.accept_group:
                        return self.str_match(self.event.message.get_plain_text())
        elif self.adapter.name == 'mirai':
            if self.dice_config.handle_all_message:
                return self.str_match(self.event.message.get_plain_text())
            elif self.event.type == 'FriendMessage' and self.dice_config.handle_friend_message:
                return self.str_match(self.event.message.get_plain_text())
            elif self.event.type == 'GroupMessage' and self.dice_config.handle_group_message:
                if self.dice_config.accept_group is None or self.event.sender.group.id in self.dice_config.accept_group:
                    return self.str_match(self.event.message.get_plain_text())
        return False

    def str_match(self, msg_str: str) -> bool:
        msg_str = msg_str.strip()
        self.msg_match = self.re_pattern.fullmatch(msg_str)
        return bool(self.msg_match)
