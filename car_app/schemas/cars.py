from pydantic import BaseModel, Field
from car_app.schemas.users import UserGet

# Validate Data

# Cars
class CarGet(BaseModel):
    id: int
    brand: str
    model: str
    year: int
    istorepair: bool
    owner_id: int

    # check while genereting
    model_config = {
        "from_attributes": True
    }
class CarCreate(BaseModel):
    brand: str
    model: str
    year: int = Field(ge=1900)
    istorepair: bool | None = None
class CarUpdate(BaseModel):
    brand: str | None = None
    model: str | None = None
    year: int | None = None
    istorepair: bool | None = None

# Get both Car and User
class CarAndUser(BaseModel):
    car: CarGet
    owner: UserGet