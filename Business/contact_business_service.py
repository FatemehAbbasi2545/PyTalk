from Common.Entities.contact import ContactInfo
from Common.Interfaces.contact_repository_interface import IContactRepository
from Common.Exceptions.custom_errors import ContactAlreadyExistsError, UserNotFoundError
from Common.DTO.response import Response

class ContactBusinessService:
    def __init__(self, contact_repository: IContactRepository):
        self.contact_repository = contact_repository
        self.current_user_contacts: list[ContactInfo] = []

    def add_contact(self, user_id: int, contact_number: str) -> Response:
        try:
            contact: ContactInfo = self.contact_repository.add_contact(user_id, contact_number)  
            return Response(True, '', contact)
        except UserNotFoundError as error:
            return Response(False, error.message)
        except ContactAlreadyExistsError as error:
            return Response(False, error.message)
        except Exception as error:
            return Response(False, "Internal Server Error!", None)  
        
    def get_user_contacts(self, user_id: int) -> Response:
        contacts: list[ContactInfo] = self.contact_repository.get_user_contacts(user_id)
        self.current_user_contacts = contacts
        return Response(True, "", contacts)
    
    def change_status(self, blocked_contacts: list[int], unblocked_contacts: list[int]) -> Response:
        try:
            self.contact_repository.change_status(blocked_contacts, unblocked_contacts)
            return Response(True, "")
        except Exception as error:
            return Response(False, error.message)


    
        
