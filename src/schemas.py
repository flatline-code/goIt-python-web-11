from datetime import date
from pydantic import BaseModel, Field, EmailStr


class ContactModel(BaseModel):
    name: str = Field(max_length=50)
    surname: str = Field(max_length=50)
    email: EmailStr
    phone_number: str = Field(max_length=50)
    birthday: date
    description: str = Field(max_length=150)

class ContactResponse(ContactModel):
    id: int
    surname: str
    email: EmailStr
    phone_number: str
    birthday: date
    description: str

    class Config:
        orm_mode = True