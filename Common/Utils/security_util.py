import hashlib

class SecurityUtil:    
    @staticmethod
    def hash_password(password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def verify(password: str, stored_hash: str) -> bool:
        """
        بررسی مطابقت پسورد وارد شده با هشی که در دیتابیس ذخیره شده
        """
        new_hash = SecurityUtil.hash_password(password)
        return stored_hash == new_hash
