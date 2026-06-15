from abc import ABC, abstractmethod
from Common.Entities.message import Message

class IMessageRepository(ABC):
    @abstractmethod
    def save_message(self, message: Message):
        pass

    @abstractmethod
    def get_history(self, sender_user_id: int, receiver_user_id: int) -> list[Message]:
        pass