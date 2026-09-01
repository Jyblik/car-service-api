from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm

from database import get_db
from car_app.models.user import User
from car_app.schemas.users import (UserGet, UserCreate, Token, UserUpdate)
from car_app.core.security import (password_hash, create_access_token, get_current_user)

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


# REGISTER
@router.post("/register", status_code=201, response_model=UserGet)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(
        User.username == user_data.username
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )
    
    new_user = User(
        username=user_data.username,
        password_hash=password_hash.hash(user_data.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

# LOGIN
@router.post("/login", response_model=Token)
def login(
    db: Session = Depends(get_db),
    # create OA2Form -> set as form_data
    form_data: OAuth2PasswordRequestForm = Depends() #get data from HTML Form | used on request
    ):
    # first() -> get the filtered user
    user = db.query(User).filter(
        User.username == form_data.username
    ).first()
    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password"
        )
    if not password_hash.verify(
        form_data.password,
        user.password_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password"
        )
    token = create_access_token(
        {"sub": user.username},
        timedelta(minutes=30)
    )

    return {"access_token": token, "token_type": "bearer"}

@router.get("/profile", response_model=UserGet)
async def profile(current_user: User = Depends(get_current_user)):
    return current_user

@router.patch("/update", response_model=UserGet)
async def patch_user(
    user_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
    ):
    updated_user = user_data.model_dump(exclude_unset=True)
    
    for fields, values in updated_user.items():
        setattr(current_user, fields, values)

    db.commit()
    db.refresh(current_user)

    return current_user