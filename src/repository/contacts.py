from typing import List
from datetime import datetime, timedelta
from sqlalchemy import and_

from sqlalchemy.orm import Session
from src.database.models import Contact, User
from src.schemas import ContactModel


async def get_contacts(skip: int, limit: int, db: Session, user: User) -> List[Contact]:
    """
    Retrieves a list of contacts for a specific user with specified pagination parameters.

    :param skip: The number of contacts to skip.
    :type skip: int
    :param limit: The maximum number of contacts to return.
    :type limit: int
    :param user: The user to retrieve contacts for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: A list of contacts.
    :rtype: List[Contact]
    """
    return db.query(Contact).filter(Contact.user_id == user.id).offset(skip).limit(limit).all()


async def create_contact(body: ContactModel, db: Session, user: User) -> Contact:
    """
    Creates a new contact for a specific user.

    :param body: The data for the contact to create.
    :type body: ContactModel
    :param user: The user to create the contact for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: The newly created contact.
    :rtype: Contact
    """
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
    """
    Retrieves a single contact with the specified ID for a specific user.

    :param contact_id: The ID of the contact to retrieve.
    :type contact_id: int
    :param user: The user to retrieve the contact for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: The contact with the specified ID, or None if it does not exist.
    :rtype: Contact | None
    """
    return db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()


async def update_contact(contact_id: int, body: ContactModel, db: Session, user: User) -> Contact | None:
    """
    Updates a single contact with the specified ID for a specific user.

    :param contact_id: The ID of the contact to update.
    :type contact_id: int
    :param body: The updated data for the contact.
    :type body: ContactModel
    :param user: The user to update the contact for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: The updated contact, or None if it does not exist.
    :rtype: Contact | None
    """
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
    """
    Removes a single contact with the specified ID for a specific user.

    :param contact_id: The ID of the contact to remove.
    :type contact_id: int
    :param user: The user to remove the contact for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: The removed contact, or None if it does not exist.
    :rtype: Contact | None
    """
    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def get_contacts_by_info(info: str, db: Session, user: User) -> List[Contact]:
    """
    The get_contacts_by_info function takes a string and returns a list of contacts that have the string in their first name, second name or email.
        Args:
            info (str): The string to search for.
            db (Session): A database session object.
            user (User): An authenticated user object.
    
    :param info: str: Pass the information that we want to search for
    :param db: Session: Create a connection to the database
    :param user: User: Get the user id from the database
    :return: A list of contacts with the specified information
    """
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
    """
    The get_birthday_per_week function returns a list of contacts whose birthday is within the next 7 days.
        Args:
            days (int): The number of days to look ahead for birthdays.
            db (Session): A database session object that can be used to query the database.
            user (User): The user who's contacts we want to query.
    
    :param days: int: Specify the number of days in which we want to get the birthdays
    :param db: Session: Access the database
    :param user: User: Get the user id of the current logged in user
    :return: A list of contacts whose birthdays are in the next 7 days
    """
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

