from abc import ABC, abstractmethod
from Common.Entities.user import User

class IUserRepository(ABC):
    @abstractmethod
    def create_user(self, user: User):
        pass

    @abstractmethod
    def get_user_by_user_name(self, user_name: str) -> User | None:
        pass

    @abstractmethod
    def change_password(self, new_password: str, user_id: int):
        pass

    
