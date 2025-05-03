
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.contact import ContactCreate, ContactUpdate, ContactInDB
from app.crud.contact import (
    create_contact, get_contacts, get_contact, update_contact,
    delete_contact, search_contacts, get_upcoming_birthdays
)
from app.auth.security import get_current_user, get_current_active_verified_user
from app.models.user import User

router = APIRouter()


@router.post("/", response_model=ContactInDB, status_code=status.HTTP_201_CREATED)
def create_new_contact(contact: ContactCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_verified_user)) -> ContactInDB:
    return create_contact(db, contact, current_user.id)


@router.get("/", response_model=List[ContactInDB])
def read_contacts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_verified_user)) -> List[ContactInDB]:
    return get_contacts(db, current_user.id, skip, limit)


@router.get("/{contact_id}", response_model=ContactInDB)
def read_contact(contact_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_verified_user)) -> ContactInDB:
    db_contact = get_contact(db, contact_id, current_user.id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact


@router.put("/{contact_id}", response_model=ContactInDB)
def update_existing_contact(contact_id: int, contact: ContactUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_verified_user)) -> ContactInDB:
    db_contact = update_contact(db, contact_id, contact, current_user.id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact


@router.delete("/{contact_id}", response_model=ContactInDB)
def delete_existing_contact(contact_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_verified_user)) -> ContactInDB:
    db_contact = delete_contact(db, contact_id, current_user.id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact


@router.get("/search/", response_model=List[ContactInDB])
def search_contacts_endpoint(query: str = Query(..., min_length=1), db: Session = Depends(get_db), current_user: User = Depends(get_current_active_verified_user)) -> List[ContactInDB]:
    return search_contacts(db, query, current_user.id)


@router.get("/birthdays/", response_model=List[ContactInDB])
def get_upcoming_birthdays_endpoint(db: Session = Depends(get_db), current_user: User = Depends(get_current_active_verified_user)) -> List[ContactInDB]:
    """
    Get contacts with birthdays in the upcoming week for the authenticated user.
    """
    return get_upcoming_birthdays(db, current_user.id)
