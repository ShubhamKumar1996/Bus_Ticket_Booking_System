from pydantic import BaseModel, Field, EmailStr


class User(BaseModel):
    firstname: str | None = Field(default=None, pattern="[a-zA-Z]{3,10}")
    lastname: str | None = Field(default=None, pattern="[a-zA-Z]{3,10}")
    email: EmailStr
    password: str = Field(min_length=4, max_length=16)
    mobile: str | None = Field(default=None, pattern="[0-9]{10}")
