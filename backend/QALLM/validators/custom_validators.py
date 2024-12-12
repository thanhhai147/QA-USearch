import re

class AdancedValidator():
    @staticmethod
    def check_user_name(user_name: str) -> bool:
        pattern = r'^[\w]+$'
        return re.fullmatch(pattern, user_name) is not None
    
    @staticmethod
    def check_password(password: str) -> bool:
        pattern = r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[!@#$%^&*()\-_=+{};:,<.>]).*$'
        return re.fullmatch(pattern, password) is not None