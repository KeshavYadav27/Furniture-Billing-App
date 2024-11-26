from decimal import Decimal

from pydantic import BaseModel, EmailStr, Field


class OurBaseModel(BaseModel):
    class Config:
        # orm_mode was renamed to from_attributes
        # orm_mode=True
        from_attribute=True

# from_attributes = True indicates that Pydantic should use attribute-style access to data, making it compatible with ORMs that use attribute access.

class ClientRequest(OurBaseModel):
    first_name: str = Field(default=None)
    last_name: str = Field(default=None)
    contact_number: str = Field(default=None)
    address: str = Field(default=None)
    description: str = Field(default=None)
    

class LoginRequest(OurBaseModel):
    email: str = Field(default=None)
    password: str = Field(default=None)
    class Config:
        the_schema = {
            "emp_demo":{
                "email":"keshavyadav516@gmail.com",
                "password":"1234"  
            }
        }

class ItemRequest(OurBaseModel):
    client_id: int = Field(default=None)
    name: str = Field(default=None)
    size: str = Field(default=None)
    quantity: int = Field(default=None)
    price_per_piece: float = Field(default=None)


class BillRequest(OurBaseModel):
    client_id: int = Field(default=None)
    bill: str = Field(default=None)

