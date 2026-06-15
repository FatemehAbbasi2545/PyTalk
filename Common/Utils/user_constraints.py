import re

class UserConstraints:
    @staticmethod
    def validate_password(password: str) -> bool:
        if len(password) < 8:
            return False
        
        # فقط شامل حروف بزرگ و کوچک، اعداد، @ و * باشه
        if not re.fullmatch(r'[a-zA-Z0-9@*]+', password):
            return False
        
        # حداقل یکی از هر کدوم
        if not re.search(r'[a-z]', password):
            return False
        if not re.search(r'[A-Z]', password):
            return False
        if not re.search(r'\d', password):
            return False
        if not re.search(r'[@*]', password):
            return False
        
        return True
    
    @staticmethod
    def validate_mobile_phone(mobile_phone: str) -> bool:
        if len(mobile_phone) != 11:
            return False                
        pattern = r"^09\d{9}$"
        return bool(re.match(pattern, mobile_phone))

        
        