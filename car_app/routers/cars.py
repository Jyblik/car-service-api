from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from car_app.core.security import get_current_user
from car_app.dependencies.dependencies import get_car_or_404, get_current_owner
from database import get_db
from car_app.models.car import Car
from car_app.models.user import User
from car_app.schemas.cars import (CarGet, CarCreate, CarUpdate, CarAndUser)

router = APIRouter(
    prefix="/cars",
    tags=["Cars"]
)

# GET
@router.get("/", response_model=list[CarGet])
async def get_cars(db: Session = Depends(get_db)):
    result = db.execute(select(Car))
    return result.scalars().all()
@router.get("/{car_id}", response_model=CarAndUser)
async def get_car(car: Car = Depends(get_car_or_404)):
    return {"car": car, "owner": car.owner}
@router.get("/mycars/", response_model=list[CarGet])
async def get_my_cars(
    current_user: User = Depends(get_current_user)
):
    return current_user.cars

# POST
@router.post("/", status_code=201, response_model=CarGet)
async def create_car(
        car: CarCreate, 
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
    ):
    new_car = Car(
        brand=car.brand,
        model=car.model,
        year=car.year,
        istorepair=car.istorepair,
        owner_id = current_user.id # server decides
    )

    db.add(new_car)
    db.commit()
    db.refresh(new_car)

    return new_car

# UPDATE
@router.put("/{car_id}", response_model=CarGet)
async def update_car(
    car_data: CarCreate,
    car: Car = Depends(get_current_owner),
    db: Session = Depends(get_db),
    ):

    car.brand = car_data.brand
    car.model = car_data.model
    car.year = car_data.year
    car.istorepair = car_data.istorepair

    db.commit()
    db.refresh(car)

    return car
@router.patch("/{car_id}", response_model=CarGet)
async def update_car_partially(
    car_data: CarUpdate,
    car: Car = Depends(get_current_owner), 
    db: Session = Depends(get_db),
    ):

    # get only full fields
    updated_car = car_data.model_dump(
        exclude_unset=True
    )
    # car.field = field: value | for all F&V in request
    for field, value in updated_car.items():
        setattr(car, field, value)

    db.commit()
    db.refresh(car)
    
    return car

# DELETE
@router.delete("/{car_id}", status_code=204)
async def delete_car(
    car: Car = Depends(get_current_owner),
    db: Session = Depends(get_db),
    ):
    
    db.delete(car)
    db.commit()