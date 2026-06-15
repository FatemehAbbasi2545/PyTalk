from Common.Entities.user import User
from Common.Interfaces.user_repository_interface import IUserRepository
from Common.Exceptions.custom_errors import UserAlreadyExistsError
from Common.Utils.user_constraints import UserConstraints
from Common.Utils.security_util import SecurityUtil
from Common.DTO.response import Response

class UserBusinessService:
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository
        self.current_user: User = None

    def register_user(self, user: User) -> Response:
        if not UserConstraints.validate_mobile_phone(user.mobile_phone):
            return Response(False, "Invalid Mobile Phone!")

        if not UserConstraints.validate_password(user.password):
            msg = '> The password must:\n> Be at least 8 characters long.\n> Contain both uppercase and lowercase English letters.\n'
            msg += '> Include numbers (0-9).\n'
            msg += '> Include at least one of the following characters: * or @.'  
            return Response(False, msg)
        
        user.password = SecurityUtil.hash_password(user.password)

        try:
            self.user_repository.create_user(user)  
            return Response(True, f"User {user.user_name} registered successfully")
        except UserAlreadyExistsError as error:
            return Response(False, error.message)
        except Exception as error:
            return Response(False, "Internal Server Error!")  
        
    def login(self, user_name: str, password: str) -> Response:
        user = self.user_repository.get_user_by_user_name(user_name)

        if not user:
            return Response(False, "No user found with this username.")
        
        if not SecurityUtil.verify(password, user.password):
            return Response(False, "Invalid password.")
        
        self.current_user = user
        return Response(True, "")
        
    def change_password(self, new_password: str) -> Response:
        if not UserConstraints.validate_password(new_password):
            msg = '> The password must:\n> Be at least 8 characters long.\n> Contain both uppercase and lowercase English letters.\n'
            msg += '> Include numbers (0-9).\n'
            msg += '> Include at least one of the following characters: * or @.'  
            return Response(False, msg)
        
        new_password = SecurityUtil.hash_password(new_password)

        try:
            self.user_repository.change_password(new_password, self.current_user.user_id)
            return Response(True, "Operation successful")
        except UserAlreadyExistsError as error:
            return Response(False, error.message)
    
        
