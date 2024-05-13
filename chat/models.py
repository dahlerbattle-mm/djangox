from django.db import models
from enum import Enum, auto

class Category(Enum):
    PRODUCT_ISSUES = auto()
    BILLING = auto()
    PARTNERSHIPS = auto()
    FEEDBACK = auto()
    OTHER = auto()

class ContactUs:
    def __init__(self, user_id, category, message):
        self.user_id = user_id
        if isinstance(category, Category):
            self.category = category
        else:
            raise ValueError("category must be an instance of Category Enum")
        self.message = message

    def __str__(self):
        return f"ContactUs(user_id={self.user_id}, category={self.category.name}, message={self.message})"
