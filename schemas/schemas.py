from datetime import date
from pydantic import BaseModel, validator, EmailStr
from typing import Optional


class UserDetail(BaseModel):
    firstname: str
    lastname: str
    phone_no: str
    email: EmailStr
    dob: Optional[date]
    address: Optional[str]

    class Config:
        orm_mode = True

    @validator('phone_no')
    def check_phone_no(cls, v):
        if (9 <= len(v) <= 13) and v.isnumeric():
            return v
        raise ValueError("Invalid Phone number! Try again")


class UpdateDetail(BaseModel):
    firstname: Optional[str]
    lastname: Optional[str]
    phone_no: Optional[str]
    email: Optional[EmailStr]
    dob: Optional[date]
    address: Optional[str]

    class Config:
        orm_mode = True

    @validator('phone_no')
    def check_phone_no(cls, v):
        if (9 <= len(v) <= 13) and v.isnumeric():
            return v
        raise ValueError("Invalid Phone number! Try again")
