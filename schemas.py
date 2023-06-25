from typing import Optional

from pydantic import BaseModel, SecretStr


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

class Settings(BaseModel):                          # Field(env_name='S_KEY')
    authjwt_secret_key: SecretStr = "5e90819cb384adba98ae70d40ab338f72ade3846be0c774444f4138bedbc76df"

class LoginModel(BaseModel):
    username: str
    password: str

class OrderModel(BaseModel):
    id: Optional[int]
    quantity: int
    order_status: Optional[str] = "PENDING"
    pizza_size: Optional[str] = "SMALL"
    flavour: Optional[str] = "PEPERONI"
    user_id: Optional[int]

    class Config:
        orm_mode = True
        schema = {
            "example": {
                "quantity": 2,
                "pizza_size": "LARGE"
            }
        }

class OrderStatusModel(BaseModel):
    order_status: Optional[str] = "PENDING"

    class Config:
        orm_mode=True
        schema = {
            "example": {
                "order_status": "PENDING"
            }
        }
