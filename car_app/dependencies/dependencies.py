from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from car_app.models.car import Car
from car_app.models.user import User
from car_app.models.detail import Detail
from database import get_db
from car_app.core.security import get_current_user


# Car
def get_car_or_404(
        car_id: int,
        db: Session = Depends(get_db)
):
    car = db.get(Car, car_id)

    if car is None:
        raise HTTPException(
            status_code=404,
            detail="Car not found"
        )
    return car

def get_current_owner(
        car: Car = Depends(get_car_or_404),
        current_user: User = Depends(get_current_user)
):
    if car.owner_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Invalid owner data"
        )
    return car

# Detail
def get_detail_or_404(
        detail_id: int,
        db: Session = Depends(get_db)
):
    detail = db.get(Detail, detail_id)

    if detail is None:
        raise HTTPException(status_code=404, detail="Not found")

    return detail

def get_current_detail_owner(
        detail: Detail = Depends(get_detail_or_404),
        current_user: User = Depends(get_current_user)
):
    if detail.owner_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Invalid owner data"
        )
    return detail