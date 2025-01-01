from aiogram.filters import BaseFilter
from aiogram.types import Message


class ChatFilter(BaseFilter):
    def __init__(self, chat_type: str):
        super().__init__()
        self.chat_type = chat_type

    async def __call__(self, message: Message, *args, **kwargs):
        if message.chat.type == self.chat_type:
            return True
