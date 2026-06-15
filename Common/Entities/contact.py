class Contact:
    def __init__(self, contact_id: int, user_id: int, audience_id: int, status: int):
        self.contact_id = contact_id 
        self.user_id = user_id
        self.audience_id = audience_id
        self.status = status

class ContactInfo:
    def __init__(self, contact_id: int, user_id: int, audience_id: int, audience_name: str, audience_phone: str, status: int):
        self.contact_id = contact_id
        self.user_id = user_id
        self.audience_id = audience_id
        self.audience_name = audience_name
        self.audience_phone = audience_phone
        self.status = status