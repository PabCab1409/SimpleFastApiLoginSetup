from pydantic import BaseModel

class Contact(BaseModel):
    name: str
    surname: str
    phone: str