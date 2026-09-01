from typing import TYPE_CHECKING
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base

# import but don't use jet
if TYPE_CHECKING:
    from car_app.models.user import User

# CAR
class Car(Base):
    # create a table
    __tablename__ = "cars"

    # id = int | unique = True
    id: Mapped[int] = mapped_column(primary_key=True)
    
    # brand = str | max_length(100)
    brand: Mapped[str] = mapped_column(String(100))

    model: Mapped[str] = mapped_column(String(100))

    year: Mapped[int] = mapped_column(default=0)

    istorepair: Mapped[bool] = mapped_column(default=False)

    # owner_id = int | users - tablename & id - int
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    # owner = User -> car.owner = user
    owner: Mapped["User"] = relationship(
        back_populates="cars"
    )