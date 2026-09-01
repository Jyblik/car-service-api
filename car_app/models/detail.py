from typing import TYPE_CHECKING
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base
if TYPE_CHECKING:
    from car_app.models.user import User

class Detail(Base):
    __tablename__ = "details"

    id: Mapped[int] = mapped_column(primary_key=True)

    typ: Mapped[str] = mapped_column(String(100))

    brand: Mapped[str] = mapped_column(String(100))

    model: Mapped[str] = mapped_column(String(100))

    isUsed: Mapped[bool] = mapped_column(default=False)
    isSold: Mapped[bool] = mapped_column(default=False)

    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    
    owner: Mapped["User"] = relationship(back_populates="details")