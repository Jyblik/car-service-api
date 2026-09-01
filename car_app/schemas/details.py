from pydantic import BaseModel

from car_app.schemas.users import UserGet

class DetailsGet(BaseModel):
    id: int
    typ: str
    brand: str
    model: str
    isUsed: bool
    isSold: bool
    owner_id: int

    model_config = {
        "from_attributes": True
    }    

class DetailsCreate(BaseModel):
    typ: str
    brand: str
    model: str
    isUsed: bool
    isSold: bool

class CarDetail(BaseModel):
    brand: str
    model: str