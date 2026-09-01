from typing import TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base

if TYPE_CHECKING:
    from car_app.models.car import Car
    from car_app.models.detail import Detail

# USER
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    username: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        index=True
        )
    
    email: Mapped[str] = mapped_column(default="me@exmple.com")

    password_hash: Mapped[str]

    # cars = all Cars -> user.cars = all cars
    cars: Mapped[list["Car"]] = relationship(
        back_populates="owner" # same dependency | cars & owner
    )
    details: Mapped[list["Detail"]] = relationship(
        back_populates="owner"
    )