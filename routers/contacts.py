from fastapi import APIRouter, HTTPException, Depends
from models.Contacts import Contact
from db import crud
from security.login import getCurrentUser
from models.user import User

router = APIRouter()

@router.get('/contacts')
async def getContacts(currentUser: User = Depends(getCurrentUser)):
   contacts = crud.get_contacts(currentUser.id)
   return contacts

@router.get('/contact/{contactName}')
async def getContact(contactName: str, currentUser: User = Depends(getCurrentUser)):
    contact = crud.get_contact(contactName)
    return contact

@router.post('/contact') 
async def createContact(contact: Contact, currentUser: User = Depends(getCurrentUser)):
    result = crud.create_contact(contact)
    return result

@router.delete("/contact/{id}", status_code=204)
async def deleteContact(id: int, currentUser: User = Depends(getCurrentUser)):
     result = crud.delete_contact(id)
     if(result == 0):
         raise HTTPException(status_code=404, detail="Object was not deleted, or not found")
     
     return "Object deleted succesfully"