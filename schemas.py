from typing import Optional

from pydantic import BaseModel


class SignUpModel(BaseModel):
    id: Optional[int]
    username: str
    email: str
    password: str
    is_staff: Optional[bool]
    is_active: Optional[bool]

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "username": "johndoe",
                "email": "johmdoe@gmail.com",
                "password": "password",
                "is_staff": False,
                "is_active": True
            }
        }

class Settings(BaseModel):
    authjwt_secret_key: str = "5e90819cb384adba98ae70d40ab338f72ade3846be0c774444f4138bedbc76df"

class LoginModel(BaseModel):
    username: str
    password: str
