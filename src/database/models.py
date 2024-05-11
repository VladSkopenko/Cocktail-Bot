import enum
from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy import Enum
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import func
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), onupdate=func.now())


class Alcohol(enum.Enum):
    LIGHT = "light"
    STRONG = "strong"
    MEDIUM = "medium"


class Taste(Base):
    __tablename__ = "tastes"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    taste: Mapped[str] = mapped_column(String(60), nullable=False)
    cocktails = relationship('Cocktail', secondary='taste_cocktails', back_populates='tastes')


class Coctail(Base):
    __tablename__ = "coctails"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    image: Mapped[str] = mapped_column(String(255), nullable=False)
    price: Mapped[float] = mapped_column(Float(asdecimal=True), nullable=False)
    author: Mapped[str] = mapped_column(String(100), nullable=False)
    alcohol_level: Mapped[Enum] = mapped_column("alcohol_level", Enum(Alcohol), nullable=False)
    tastes = relationship('Taste', secondary='taste_cocktails', back_populates='cocktails')


class TasteCoctail(Base):
    __tablename__ = "taste_coctails"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    taste_id: Mapped[int] = mapped_column(ForeignKey("tastes.id"), nullable=False)
    coctail_id: Mapped[int] = mapped_column(ForeignKey("coctails.id"), nullable=False)
