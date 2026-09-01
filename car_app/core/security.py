import os
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone

from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException

from database import get_db
from car_app.models.user import User
import jwt
from pwdlib import PasswordHash

load_dotenv()
# PASSWORD HASH

password_hash = PasswordHash.recommended()

# KEYS
SECRET_KEY = os.getenv("SECRET_KEY")
# NONE CHECK
if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY is not set")

ALGORITHM = os.getenv("ALGORITHM", "HS256")

# TOKEN

# data = user | expires_delta = 30m
def create_access_token(data: dict, expires_delta: timedelta):
    # copy user -> sub: user NOT exp: user
    to_encode = data.copy()

    # 17:00 -> 17:30
    expire = datetime.now(timezone.utc) + expires_delta

    # add when expires
    to_encode.update({
        "exp": expire
    })

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


# Get Access Token - oa2 = /users/login/Bearer...
oa2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

# GET USER

def get_current_user(
        token: str = Depends(oa2_scheme),
        db: Session = Depends(get_db)
):
    # jwt.decode - verify TOKEN(request) & KEY(server) | get sub: /// & exp: ///
    try:
        check = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        # sub: name
        username = check.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    
    # get user by username
    user = db.query(User).filter(
        User.username == username
    ).first()

    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    
    # return user -> logged
    return user