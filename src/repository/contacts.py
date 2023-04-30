from typing import List
from datetime import datetime, timedelta
from sqlalchemy import and_

from sqlalchemy.orm import Session
from src.database.models import Contact, User
from src.schemas import ContactModel


async def get_contacts(skip: int, limit: int, db: Session, user: User) -> List[Contact]:
    return db.query(Contact).filter(Contact.user_id == user.id).offset(skip).limit(limit).all()


async def create_contact(body: ContactModel, db: Session, user: User) -> Contact:
    contact = Contact(name=body.name,
                      surname=body.surname,
                      email=body.email,
                      phone_number=body.phone_number,
                      birthday=body.birthday,
                      description = body.description,
                      user_id=user.id)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def get_contact(contact_id: int, db: Session, user: User) -> Contact:
    return db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()


async def update_contact(contact_id: int, body: ContactModel, db: Session, user: User) -> Contact | None:
    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if contact:
        contact.name = body.name
        contact.surname = body.surname
        contact.email = body.email
        contact.phone_number = body.phone_number
        contact.birthday = body.birthday
        contact.description = body.description
        db.commit()
    return contact


async def remove_contact(contact_id: int, db: Session, user: User) -> Contact | None:
    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def get_contacts_by_info(info: str, db: Session, user: User) -> List[Contact]:
    response = []
    info_by_name = db.query(Contact).filter(and_(Contact.name.like(f'%{info}%'), Contact.user_id == user.id)).all()
    if info_by_name:
        for contact in info_by_name:
            response.append(contact)
    info_by_surname = db.query(Contact).filter(and_(Contact.name.like(f'%{info}%'), Contact.user_id == user.id)).all()
    if info_by_surname:
        for contact in info_by_surname:
            response.append(contact)
    info_by_email = db.query(Contact).filter(and_(Contact.name.like(f'%{info}%'), Contact.user_id == user.id)).all()
    if info_by_email:
        for contact in info_by_email:
            response.append(contact)
    return response

async def get_birthday_per_week(days: int, db: Session, user: User):
    response = []
    all_contacts = db.query(Contact).filter(Contact.user_id == user.id).all()
    today = datetime.now().date()
    delta = timedelta(days=days)

    for contact in all_contacts:
        contact_next_birthday = datetime(year=today.year,
                                         month=contact.birthday.month,
                                         day=contact.birthday.day).date()
        if contact_next_birthday < today:
            continue
        if contact_next_birthday - today > delta:
            continue

        response.append(contact)
    return response

