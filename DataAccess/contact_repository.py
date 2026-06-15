import sqlite3
from Common.Entities.contact import Contact, ContactInfo
from Common.Interfaces.contact_repository_interface import IContactRepository
from Common.Exceptions.custom_errors import ContactAlreadyExistsError, UserNotFoundError
from Common.Enums.contact_status import ContactStatus

class ContactRepository(IContactRepository):
    def __init__(self, db_name):
        self.db_name = db_name
        self.create_table()

    def get_connection(self):
        return sqlite3.connect(self.db_name)
    
    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS Contact (
            contact_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            audience_id INTEGER NOT NULL,
            status INT DEFAULT 1 NOT NULL,
            FOREIGN KEY (user_id) REFERENCES User(UserId),
            FOREIGN KEY (audience_id) REFERENCES User(UserId),
            UNIQUE(user_id, audience_id)
        )
        """
        with self.get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()

    def add_contact(self, user_id: int, contact_number: str) -> ContactInfo | None:        
        try:
            with self.get_connection() as connection:
                cursor = connection.cursor()

                cursor.execute("SELECT * FROM User WHERE MobilePhone = ?", (contact_number,))
                user_data = cursor.fetchone()

                if not user_data:
                    raise UserNotFoundError(message='No registered user with this phone number.')
                
                audience_id = user_data[0]   
                contact = Contact(None, user_id, audience_id, status=ContactStatus.active)         

                cursor.execute("SELECT 1 FROM Contact WHERE user_id = ? and audience_id = ?", (contact.user_id, contact.audience_id,))
                if cursor.fetchone():
                    raise ContactAlreadyExistsError()
                
                query = "INSERT INTO Contact (user_id, audience_id) VALUES (?, ?)"
    
                cursor.execute(query, (contact.user_id, contact.audience_id))
                contact.contact_id = cursor.lastrowid

                query = """
                    SELECT c.contact_id, c.user_id, c.audience_id, audience.UserName as audience_name, audience.MobilePhone as audience_phone
                    FROM Contact c 
                    JOIN User u ON u.UserId = c.user_id
                    JOIN User audience ON audience.UserId = c.audience_id
                    WHERE c.contact_id = ? 
                """
                cursor.execute(query, (contact.contact_id,))
                result = cursor.fetchone()
                connection.commit()

                return ContactInfo(result[0], result[1], result[2], result[3], result[4], 1) if result else None
        except sqlite3.IntegrityError:
            raise ContactAlreadyExistsError()

    def get_user_contacts(self, user_id: int) -> list[ContactInfo]:
        """جستجوی لیست تماس های یک کاربر مشخص"""
        query = """
            SELECT c.contact_id, c.user_id, c.audience_id, audience.UserName as audience_name, audience.MobilePhone as audience_phone, c.status
            FROM User u
            JOIN Contact c ON c.user_id = u.UserId
            JOIN User audience ON audience.UserId = c.audience_id
            WHERE u.UserId = ?
        """
        with self.get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(query, (user_id,))
            contacts = cursor.fetchall()
            if contacts:
                result = [] 
                for c in contacts:
                    result.append(ContactInfo(c[0], c[1], c[2], c[3], c[4], c[5]))
                return result
        return []
    
    def change_status(self, blocked_contacts: list[int], unblocked_contacts: list[int]):        
        try:
            with self.get_connection() as connection:
                cursor = connection.cursor()

                # for x in blocked_contacts:
                #     query = "UPDATE Contact SET status = 2 WHERE contact_id = ?"
                #     cursor.execute(query, (x))

                if len(blocked_contacts) > 0:
                    placeholders = ",".join("?" * len(blocked_contacts))
                    cursor.execute(
                        f"UPDATE Contact SET status = 2 WHERE contact_id IN ({placeholders})",
                        blocked_contacts
                    )

                if len(unblocked_contacts) > 0:
                    placeholders = ",".join("?" * len(unblocked_contacts))
                    cursor.execute(
                        f"UPDATE Contact SET status = 1 WHERE contact_id IN ({placeholders})",
                        unblocked_contacts
                    )
        except sqlite3.DatabaseError as error:
            raise Exception(error)
            
            


                
