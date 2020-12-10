from decimal import Decimal
from typing import Optional

from pydantic import BaseModel
from pydantic.networks import EmailStr


class UserBase(BaseModel):
    email: EmailStr
    is_active: bool = True
    first_name: str = None
    last_name: str = None
    address: str = None


class UserAdmin(UserBase):
    id: int = None
    is_superuser: bool = False
    password: Optional[str] = None

    class Config:
        orm_mode = True


class UserOut(UserAdmin):
    pass


class UserCreate(UserBase):
    password: str
    is_superuser: bool

    class Config:
        orm_mode = True


class UserEdit(UserBase):
    password: Optional[str] = None

    class Config:
        orm_mode = True


class User(UserBase):
    id: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str = None
    permissions: str = "user"


class ItemBase(BaseModel):
    name: str
    description: Optional[str] = None
    volume: int
    price: Optional[Decimal] = None
    local_id: int


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int

    class Config:
        orm_mode = True


class LocalBase(BaseModel):
    volume: int
    coordinate: str


class LocalCreate(LocalBase):
    ...


class Local(LocalBase):
    id: int
    items: list[Item] = []

    class Config:
        orm_mode = True
