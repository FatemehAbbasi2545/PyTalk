from Common.Entities.message import Message
from Common.Interfaces.message_repository_interface import IMessageRepository
from Common.DTO.response import Response

class MessageBusinessService:
    def __init__(self, message_repository: IMessageRepository):
        self.message_repository = message_repository

    def save_message(self, message: Message) -> Response:
        try:
            self.message_repository.save_message(message)  
            return Response(True, '', message)
        except Exception as error:
            return Response(False, error.message)

    def get_history(self, sender_user_id: int, receiver_user_id: int) -> Response:
        chat_history = self.message_repository.get_history(sender_user_id, receiver_user_id)
        return Response(True, "", chat_history)

    
        
