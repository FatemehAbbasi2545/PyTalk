from abc import ABC, abstractmethod
from Common.Entities.contact import Contact, ContactInfo

class IContactRepository(ABC):
    @abstractmethod
    def add_contact(self, user_id: int, contact_number: str) -> Contact:
        pass

    @abstractmethod
    def get_user_contacts(self, user_id: int) -> list[ContactInfo]:
        pass

    @abstractmethod
    def change_status(self, blocked_contacts: list[int], unblocked_contacts: list[int]):
        pass

    
