"""
User Domain Model
-----------------
Internal representation of user entity.
"""

class User:
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email