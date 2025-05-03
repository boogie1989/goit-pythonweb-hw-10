"""
CRUD (Create, Read, Update, Delete) operations for database interactions.
"""
from app.crud.contact import (
    create_contact, get_contacts, get_contact, update_contact,
    delete_contact, search_contacts, get_upcoming_birthdays
)

from app.crud.user import (
    create_user, get_user, get_user_by_email,
    get_users, update_user, update_user_avatar, verify_user, delete_user
)

# Export CRUD operations
__all__ = [
    # Contact operations
    "create_contact",
    "get_contacts",
    "get_contact",
    "update_contact",
    "delete_contact",
    "search_contacts",
    "get_upcoming_birthdays",
    
    # User operations
    "create_user",
    "get_user",
    "get_user_by_email",
    "get_users",
    "update_user",
    "update_user_avatar",
    "verify_user",
    "delete_user"
]
