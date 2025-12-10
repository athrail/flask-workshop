from typing import Optional, List
from sqlalchemy import ForeignKey, String, Integer
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship


class Base(DeclarativeBase):
    pass


class Client(Base):
    __tablename__ = "clients"

    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(30))
    phone: Mapped[str] = mapped_column(String(15), unique=True)
    email: Mapped[Optional[str]] = mapped_column(String(30))
    cars: Mapped[List["Car"]] = relationship(back_populates="owner")

    def __repr__(self) -> str:
        return f"Client(id={self.id}, fn={self.full_name})"


class Car(Base):
    __tablename__ = "cars"

    id: Mapped[int] = mapped_column(primary_key=True)
    plate: Mapped[str] = mapped_column(String(15))
    owner_id: Mapped[int] = mapped_column(ForeignKey("clients.id"))
    owner: Mapped["Client"] = relationship(back_populates="cars")
    maker_id: Mapped[int] = mapped_column(ForeignKey("makers.id"))
    maker: Mapped["Maker"] = relationship()
    model_id: Mapped[int] = mapped_column(ForeignKey("models.id"))
    model: Mapped["Model"] = relationship()

    def __repr__(self) -> str:
        return f"Car(plate={self.plate}, owner={self.owner.full_name}, maker={self.maker.name}, model={self.model.name})"


class Maker(Base):
    __tablename__ = "makers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    models: Mapped[List["Model"]] = relationship(back_populates="maker")

    def __repr__(self) -> str:
        return f"Maker(name={self.name})"


class Model(Base):
    __tablename__ = "models"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    production_start: Mapped[int] = mapped_column(Integer)
    production_end: Mapped[int] = mapped_column(Integer)
    maker_id: Mapped[int] = mapped_column(ForeignKey("makers.id"))
    maker: Mapped["Maker"] = relationship(back_populates="models")


class Producer(Base):
    __tablename__ = "producers"

    id: Mapped[int] = mapped_column(primary_key=True)
    parts: Mapped[List["Part"]] = relationship(back_populates="producer")


class Part(Base):
    __tablename__ = "parts"

    id: Mapped[int] = mapped_column(primary_key=True)
    producer_id: Mapped[int] = mapped_column(ForeignKey("producers.id"))
    producer: Mapped["Producer"] = relationship(back_populates="parts")
