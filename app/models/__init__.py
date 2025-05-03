"""
SQLAlchemy ORM model definitions.
"""
from app.models.contact import Contact
from app.models.user import User

# Export models
__all__ = ["Contact", "User"]
