from pydantic import BaseModel, Field, EmailStr


class User(BaseModel):
    firstname: str = Field(pattern="[a-zA-Z]{3,10}")
    lastname: str = Field(pattern="[a-zA-Z]{3,10}")
    email: EmailStr
    password: str = Field(min_length=4, max_length=16)
    mobile: str = Field(pattern="[0-9]{10}")