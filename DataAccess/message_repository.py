import sqlite3
from Common.Entities.message import Message
from Common.Interfaces.message_repository_interface import IMessageRepository

class MessageRepository(IMessageRepository):
    def __init__(self, db_name):
        self.db_name = db_name
        self.create_table()

    def get_connection(self):
        return sqlite3.connect(self.db_name)
    
    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS Message (
            message_id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender_id INTEGER NOT NULL,
            receiver_id INTEGER NOT NULL,
            content TEXT NOT NULL,
            timestamp DATETIME NOT NULL,
            FOREIGN KEY (sender_id) REFERENCES User(UserId),
            FOREIGN KEY (receiver_id) REFERENCES User(UserId)
        )
        """
        with self.get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()

    def save_message(self, message: Message):
        query = "INSERT INTO Message (sender_id, receiver_id, content, timestamp) VALUES (?, ?, ?, ?)"
        try:
            with self.get_connection() as connection:
                cursor = connection.cursor()
                cursor.execute(query, (message.sender_id, message.receiver_id, message.content, message.timestamp))
                message.message_id = cursor.lastrowid
                connection.commit()
        except sqlite3.DatabaseError:
            raise Exception('"Failed to send message".')

    def get_history(self, sender_user_id: int, receiver_user_id: int) -> list[Message]:
        query = """
        SELECT message_id, sender_id, receiver_id, content, timestamp FROM Message 
        WHERE (sender_id = ? AND receiver_id = ?) OR (sender_id = ? AND receiver_id = ?)
        ORDER BY message_id ASC
        """
        with self.get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(query, (sender_user_id, receiver_user_id, receiver_user_id, sender_user_id))
            messages = cursor.fetchall()
            if messages:
                result = [] 
                for msg in messages:
                    result.append(Message(msg[0], msg[1], msg[2], msg[3], msg[4]))
                return result
        return []