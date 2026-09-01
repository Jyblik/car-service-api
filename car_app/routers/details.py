from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, or_
from sqlalchemy.orm import Session

from database import get_db
from car_app.core.security import get_current_user
from car_app.dependencies.dependencies import get_detail_or_404
from car_app.models.user import User
from car_app.models.detail import Detail
from car_app.schemas.details import (DetailsGet, DetailsCreate, CarDetail)

router = APIRouter(
    prefix="/details",
    tags=["Details"]
)

# GET
@router.get("/", response_model=list[DetailsGet])
async def get_details(
    db: Session = Depends(get_db)
):
    details = db.execute(select(Detail))
    return details.scalars().all()

@router.get("/{detail.id}", response_model=DetailsGet)
async def get_detail(detail: Detail = Depends(get_detail_or_404)):
    return detail

@router.get("/mydetails", response_model=list[DetailsGet])
async def my_details(current_user: User = Depends(get_current_user)):
    return current_user.details

# SIMMILAR
@router.post("/simmilar_details", response_model=list[DetailsGet])
async def simillar(detail_data: CarDetail, db: Session = Depends(get_db)):
    details = db.query(Detail).filter(or_(
        Detail.brand == detail_data.brand,
        Detail.model == detail_data.model
    )
    ).filter(Detail.isSold == False)

    return details.all()

# POST
@router.post("/add", status_code=201, response_model=DetailsGet)
async def add_detail(
    detail_data: DetailsCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)

):
    new_detail = Detail(
        typ=detail_data.typ,
        brand=detail_data.brand,
        model=detail_data.model,
        isUsed=detail_data.isUsed,
        isSold=detail_data.isSold,
        owner_id=current_user.id
    )

    db.add(new_detail)
    db.commit()
    db.refresh(new_detail)

    return new_detail

@router.delete("/{detail_id}", status_code=204)
async def remove_detail(
    detail: Detail = Depends(get_detail_or_404),
    db: Session = Depends(get_db)
    ):
    db.delete(detail)
    db.commit()