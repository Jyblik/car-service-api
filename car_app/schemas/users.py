from pydantic import BaseModel

class UserGet(BaseModel):
    id: int
    username: str
    email: str
class UserCreate(BaseModel):
    username: str 
    password: str 
    email: str
class UserUpdate(BaseModel): 
    username: str | None = None
    email: str | None = None
class Token(BaseModel):
    access_token: str
    token_type: str