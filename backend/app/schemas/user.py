from pydantic import BaseModel


class UserCreate(BaseModel):
    email: str
    password: str

    class Config:
        from_attributes = True


class User(UserCreate):
    id: int
    is_active: bool
    is_admin: bool

    class Config:
        from_attributes = True


class UserResponse(User):
    token: str

    class Config:
        from_attributes = True
