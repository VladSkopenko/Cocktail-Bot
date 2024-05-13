import enum
from datetime import date

from sqlalchemy import BigInteger
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
    created_at: Mapped[date] = mapped_column(
        "created_at", DateTime, default=func.now(), nullable=True
    )
    updated_at: Mapped[date] = mapped_column(
        "updated_at", DateTime, default=func.now(), onupdate=func.now(), nullable=True
    )


class Banner(Base):
    __tablename__ = "banner"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(15), unique=True)
    image: Mapped[str] = mapped_column(String(150), nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)


class Category(Base):
    __tablename__ = "category"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)


class Alcohol(enum.Enum):
    LIGHT = "light"
    STRONG = "strong"
    MEDIUM = "medium"


class Taste(Base):
    __tablename__ = "tastes"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    taste: Mapped[str] = mapped_column(String(60), nullable=False)
    cocktails = relationship(
        "Cocktail", secondary="taste_cocktails", back_populates="tastes"
    )


class Cocktail(Base):
    __tablename__ = "cocktails"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    image: Mapped[str] = mapped_column(String(255), nullable=False)
    price: Mapped[float] = mapped_column(Float(asdecimal=True), nullable=False)
    author: Mapped[str] = mapped_column(String(100), nullable=True)

    category_id: Mapped[int] = mapped_column(
        ForeignKey("category.id", ondelete="CASCADE"), nullable=False
    )
    category: Mapped["Category"] = relationship(backref="product")

    alcohol_level: Mapped[Enum] = mapped_column(
        "alcohol_level", Enum(Alcohol), nullable=True
    )
    tastes = relationship(
        "Taste", secondary="taste_cocktails", back_populates="cocktails"
    )


class TasteCoctail(Base):
    __tablename__ = "taste_cocktails"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    taste_id: Mapped[int] = mapped_column(ForeignKey("tastes.id"), nullable=False)
    cocktail_id: Mapped[int] = mapped_column(ForeignKey("cocktails.id"), nullable=False)


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    first_name: Mapped[str] = mapped_column(String(150), nullable=True)
    last_name: Mapped[str] = mapped_column(String(150), nullable=True)
    phone: Mapped[str] = mapped_column(String(13), nullable=True)


class Cart(Base):
    __tablename__ = 'cart'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey('product.id', ondelete='CASCADE'), nullable=False)
    quantity: Mapped[int]

    user: Mapped['User'] = relationship(backref='cart')
    cocktail: Mapped['Cocktail'] = relationship(backref='cart')
