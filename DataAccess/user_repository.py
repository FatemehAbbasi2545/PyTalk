import sqlite3
from Common.Entities.user import User
from Common.Interfaces.user_repository_interface import IUserRepository
from Common.Exceptions.custom_errors import UserAlreadyExistsError

class UserRepository(IUserRepository):
    def __init__(self, db_name):
        self.db_name = db_name
        self.create_table()

    def get_connection(self):
        return sqlite3.connect(self.db_name)
    
    def create_table(self):
        """ایجاد جدول کاربر در صورت عدم وجود"""
        query = """
        CREATE TABLE IF NOT EXISTS User (
            UserId INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT NOT NULL,
            UserName TEXT UNIQUE NOT NULL,
            Password TEXT NOT NULL,
            MobilePhone TEXT UNIQUE NOT NULL
        )
        """
        with self.get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()

    def create_user(self, user: User):
        """ذخیره یک کاربر جدید در دیتابیس"""
        query = "INSERT INTO User (Name, UserName, Password, MobilePhone) VALUES (?, ?, ?, ?)"
        try:
            with self.get_connection() as connection:
                cursor = connection.cursor()

                cursor.execute("SELECT 1 FROM User WHERE UserName = ?", (user.user_name,))
                if cursor.fetchone():
                    raise UserAlreadyExistsError(message="Username is already taken.")
    
                cursor.execute("SELECT 1 FROM User WHERE MobilePhone = ?", (user.mobile_phone,))
                if cursor.fetchone():
                    raise UserAlreadyExistsError(message='A user with this phone number already exists.')
    
                cursor.execute(query, (user.name, user.user_name, user.password, user.mobile_phone))
                user.user_id = cursor.lastrowid
                connection.commit()
        except sqlite3.IntegrityError:
            raise UserAlreadyExistsError('UserName or mobile phone already exists.')

    def get_user_by_user_name(self, user_name: str) -> User | None:
        """جستجوی کاربر بر اساس نام کاربری"""
        query = "SELECT * FROM User WHERE UserName = ?"
        with self.get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(query, (user_name,))
            user_data = cursor.fetchone()
            if user_data:
                return User(id=user_data[0], name=user_data[1], user_name=user_data[2], password=user_data[3], mobile_phone=user_data[4])
        return None
    
    def change_password(self, new_password: str, user_id: int):
        try:
            with self.get_connection() as connection:
                cursor = connection.cursor()
                query = "UPDATE User SET Password = ? WHERE UserId = ?"
                cursor.execute(query, (new_password, user_id))
        except sqlite3.DatabaseError as error:
            raise Exception(error)
