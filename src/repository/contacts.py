from typing import List

from sqlalchemy.orm import Session
from src.database.models import Contact
from src.schemas import ContactModel


async def get_contacts(skip: int, limit: int, db: Session) -> List[Contact]:
    return db.query(Contact).offset(skip).limit(limit).all()

async def create_contact(body: ContactModel, db: Session) -> Contact:
    contact = Contact(**body.dict())
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact

async def get_contact(contact_id: int, db: Session) -> Contact:
    return db.query(Contact).filter(Contact.id == contact_id).first()

async def update_contact(contact_id: int, body: ContactModel, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        contact.name = body.name
        contact.surname = body.surname
        contact.email = body.email
        contact.birthday = body.birthday
        contact.description = body.description
        db.commit()
    return contact

async def remove_contact(contact_id: int, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact

async def get_contacts_by_info(info: str, db: Session) -> List[Contact]:
    response = []
    info_by_name = db.query(Contact).filter(Contact.name.like(f'%{info}%')).all()
    if info_by_name:
        for contact in info_by_name:
            response.append(contact)
    info_by_surname = db.query(Contact).filter(Contact.surname.like(f'%{info}%')).all()
    if info_by_surname:
        for contact in info_by_surname:
            response.append(contact)
    info_by_email = db.query(Contact).filter(Contact.email.like(f'%{info}%')).all()
    if info_by_email:
        for contact in info_by_email:
            response.append(contact)
            
    return response