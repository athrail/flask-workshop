from typing import Optional, List
from sqlalchemy import Column, ForeignKey, String, Integer, Table
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
    jobs: Mapped[List["Job"]] = relationship(back_populates="car")

    def __repr__(self) -> str:
        return f"Car(plate={self.plate}, owner={self.owner.full_name}, maker={self.maker.name}, model={self.model.name})"


class Maker(Base):
    __tablename__ = "makers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    models: Mapped[List["Model"]] = relationship(back_populates="maker")

    def __repr__(self) -> str:
        return f"Maker(name={self.name})"


job_part_association_table = Table(
    "job_part",
    Base.metadata,
    Column("job_id", ForeignKey("jobs.id")),
    Column("part_id", ForeignKey("parts.id")),
)


class Job(Base):
    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(String())
    car_id: Mapped[int] = mapped_column(ForeignKey("cars.id"))
    car: Mapped["Car"] = relationship()
    parts: Mapped[List["Part"]] = relationship(secondary=job_part_association_table)


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
    name: Mapped[str] = mapped_column(String(20))
    parts: Mapped[List["Part"]] = relationship(back_populates="producer")


class Part(Base):
    __tablename__ = "parts"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    number: Mapped[str] = mapped_column(String(50))
    producer_id: Mapped[int] = mapped_column(ForeignKey("producers.id"))
    producer: Mapped["Producer"] = relationship(back_populates="parts")
