from alicebot.exception import AdapterTimeout

from plugins.alicebot_plugin_public import BasePlugin

from .config import Config


class Repeater(BasePlugin[Config]):
    priority: int = 2
    plugin_config_class: Config = Config
    try_times: int = 0

    async def handle(self) -> None:
        try:
            await self.get(self.same_sender, timeout=self.plugin_config.get_timeout)
        except AdapterTimeout:
            pass
        else:
            await self.event.reply(self.event.message)

    def same_sender(self, event):
        if self.try_times >= 2:
            raise AdapterTimeout
        flag = False
        if event.adapter.name == 'cqhttp':
            if event.type == 'message':
                if event.message_type == 'private':
                    flag = event.user_id == self.event.user_id
                elif event.message_type == 'group':
                    flag = event.group_id == self.event.group_id
        elif event.adapter.name == 'mirai':
            if event.type == 'FriendMessage':
                flag = event.sender.id == self.event.sender.id
            elif event.type == 'GroupMessage':
                flag = event.sender.group.id == self.event.sender.group.id
        if flag:
            self.try_times += 1
            return event.message == self.event.message
        else:
            return False

    def str_match(self, msg_str: str) -> bool:
        return True
