from pydantic import BaseModel

class Users(BaseModel):
    name :str
    email:str

class UserCreate(Users):
    pass


class User(Users):
    id: int

    class Config:
        orm_mode = True