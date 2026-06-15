from datetime import datetime

class Message:
    def __init__(self, message_id: int, sender_id: int, receiver_id: int, content: str, timestamp=datetime.now()):
        self.message_id = message_id       
        self.sender_id = sender_id       
        self.receiver_id = receiver_id    
        self.content = content            
        self.timestamp = timestamp 