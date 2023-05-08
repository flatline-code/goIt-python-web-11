import unittest
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from src.database.models import Contact, User
from src.schemas import ContactModel
from src.repository.contacts import (
    get_contacts,
    get_contacts_by_info,
    get_contact,
    create_contact,
    remove_contact,
    update_contact,
    get_birthday_per_week,
)


class TestContacts(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)

    async def test_get_contacts(self):
        contacts = [Contact(), Contact(), Contact()]
        self.session.query().filter().offset().limit().all.return_value = contacts
        result = await get_contacts(skip=0, limit=10, user=self.user, db=self.session)
        self.assertEqual(result, contacts)

    async def test_get_contact(self):
        contact = Contact()
        self.session.query().filter().first.return_value = contact
        result = await get_contact(contact_id=1, user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_get_contact_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await get_contact(contact_id=1, user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_create_contact(self):
         body = ContactModel(name="Test",
                                  surname="Surname",
                                  email="test@email.com",
                                  phone="111222333",
                                  birthday='1990-01-01')
 
         result = await create_contact(body=body, user=self.user, db=self.session)
         self.assertEqual(result.name, body.name)
         self.assertEqual(result.surname, body.surname)
         self.assertEqual(result.email, body.email)
         self.assertTrue(hasattr(result, "id"))

    async def test_update_contact(self):
        contact = Contact()
        body = ContactModel(name="Test",
                                 surname="Surname",
                                 email="test@email.com",
                                 phone="111222333",
                                 birthday='1990-01-01')
        self.session.query().filter().first.return_value = contact
        self.session.commit.return_value = None
        result = await update_contact(contact_id=1, body=body, user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_update_contact_not_found(self):
        body = ContactModel(name="Test",
                                 surname="Surname",
                                 email="test@email.com",
                                 phone="111222333",
                                 birthday='1990-01-01')
        self.session.query().filter().first.return_value = None
        self.session.commit.return_value = None
        result = await update_contact(contact_id=1, body=body, user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_remove_contact(self):
        contact = Contact()
        self.session.query().filter().first.return_value = contact
        result = await remove_contact(contact_id=1,
                                      user=self.user,
                                      db=self.session)
        self.assertEqual(result, contact)

    async def test_remove_contact_not_found(self):
        self.session.query().filter().first.return_value = None

        result = await remove_contact(contact_id=1,
                                      user=self.user,
                                      db=self.session)
        self.assertIsNone(result)

    async def test_get_contacts_by_info(self):
        contacts = [Contact(), Contact()]
        self.session.query().filter().all.return_value = contacts
        result = await get_contacts_by_info(info="test@email.com", db=self.session, user=self.user)
        self.assertEqual(result, contacts)

    async def test_get_birthday_per_week(self):
        contacts = []
        self.session.query().filter().all.return_value = contacts
        result = await get_birthday_per_week(days=5, db=self.session, user=self.user)
        self.assertEqual(result, contacts)


if __name__ == '__main__':
    unittest.main()
