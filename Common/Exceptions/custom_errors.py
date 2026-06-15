class UserAlreadyExistsError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class ContactAlreadyExistsError(Exception):
    def __init__(self, message='This contact is already in your contact list.'):
        self.message = message
        super().__init__(self.message)

class UserNotFoundError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)