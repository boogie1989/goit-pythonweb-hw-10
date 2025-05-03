"""
Contact schemas for data validation and serialization.
"""
from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional


class ContactBase(BaseModel):
    """
    Base schema for contact data.
    """
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    birthday: date
    additional_info: Optional[str] = None


class ContactCreate(ContactBase):
    """
    Schema for creating a new contact.
    """
    pass


class ContactUpdate(ContactBase):
    """
    Schema for updating an existing contact.
    """
    pass


class ContactInDB(ContactBase):
    """
    Schema for contact data as stored in the database.
    """
    id: int

    class Config:
        orm_mode = True  # For Pydantic v1
