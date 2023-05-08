from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import User
from src.schemas import ContactModel, ContactResponse
from src.repository import contacts as repository_contacts
from src.services.auth import auth_service

router = APIRouter(prefix='/contacts', tags=['contacts'] )


@router.get("/", response_model=List[ContactResponse], description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def read_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
                     current_user: User = Depends(auth_service.get_current_user)):
    """
    The read_contacts function returns a list of contacts.
    :param skip: int: Skip a number of records in the database
    :param limit: int: Limit the number of contacts returned
    :param db: Session: Pass a database session to the function
    :param current_user: User: Get the user who is making the request
    :return: A list of contacts, which is the same as the return type of get_contacts
    """
    contacts = await repository_contacts.get_contacts(skip, limit, db, current_user)
    return contacts

@router.post("/", response_model=ContactResponse, description='No more than 1 requests per minute',
            dependencies=[Depends(RateLimiter(times=1, seconds=60))], status_code=status.HTTP_201_CREATED)
async def create_contact(body: ContactModel, db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    """
    The create_contact function creates a new contact in the database.
    :param body: ContactModel: Define the body of the request
    :param db: Session: Pass the database session to the function
    :param current_user: User: Get the current user from the database
    :return: A contact object
    """
    return await repository_contacts.create_contact(body, db, current_user)

@router.get("/{contact_id}", response_model=ContactResponse)
async def read_contact(contact_id: int, db: Session = Depends(get_db),
                       current_user: User = Depends(auth_service.get_current_user)):
    """
    The read_contact function is used to read a single contact from the database.
    It takes in an integer representing the ID of the contact, and returns a Contact object.
    :param contact_id: int: Specify the contact id
    :param db: Session: Pass a database session to the function
    :param current_user: User: Pass the current user to the function
    :return: A contact object
    """
    contact = await repository_contacts.get_contact(contact_id, db, current_user)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact

@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(body: ContactModel, contact_id: int, db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    """
    The update_contact function updates a contact in the database.
    The function takes three arguments:
        - contact_id: an integer representing the id of the contact to be updated.
        - body: a ContactModel object containing information about what fields are being updated and their new values.  This is passed as JSON data in the request body, so it must be deserialized into a ContactInputModel object before it can be used by this function.  See https://fastapi.tiangolo.com/tutorial/body-parameters/#pydantic-models for more details on how to do this with Fast
    :param contact_id: int: Identify the contact to be updated
    :param body: ContactModel: Define the body of the request
    :param db: Session: Pass the database session to the function
    :param current_user: User: Get the user that is currently logged in
    :return: The updated contact
    """
    contact = await repository_contacts.update_contact(contact_id, body, db, current_user)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact

@router.delete("/{contact_id}", response_model=ContactResponse)
async def remove_contact(contact_id: int, db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    """
    The remove_contact function removes a contact from the database.
    :param contact_id: int: Specify the contact to be deleted
    :param db: Session: Access the database
    :param current_user: User: Get the user that is currently logged in
    :return: The contact that was deleted
    """
    contact = await repository_contacts.remove_contact(contact_id, db, current_user)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact

@router.get("/find/{info}", response_model=List[ContactResponse])
async def find_contacts_by_info(info: str, db: Session = Depends(get_db), 
                                current_user: User = Depends(auth_service.get_current_user)):
    """
    The find_contacts_by_info function is used to find contacts by some info.
        Args:
            info (str): The contacts's name, email or phone number.
    
    :param info: str: Pass the search string to the function
    :param db: Session: Get the database session
    :param current_user: User: Get the current user
    :return: A list of contacts
    """
    contacts = await repository_contacts.get_contacts_by_info(info, db, current_user)
    if contacts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contacts not found")
    return contacts

@router.get("/birthday/{days}", response_model=List[ContactResponse])
async def find_birthday_per_week(days: int, db: Session = Depends(get_db), 
                                 current_user: User = Depends(auth_service.get_current_user)):
    """
    The find_birthday_per_week function returns a list of users that have their birthday in the next 7 days.
        The function takes an integer as input, which is the number of days to look ahead for birthdays.
        It then queries the database and returns a list of users with their birthday in that time frame.
    
    :param days: int: Specify the amount of days that we want to search for birthdays
    :param db: Session: Inject the database session into the function
    :param current_user: User: Get the current user
    :return: A list of users with a birthday in the next 7 days
    """
    contacts = await repository_contacts.get_birthday_per_week(days, db, current_user)
    if contacts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contacts not found")
    return contacts
