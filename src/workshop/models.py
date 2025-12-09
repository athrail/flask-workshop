from typing import Optional
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped

class Base(DeclarativeBase):
    pass

class Client(Base):
    __tablename__ = "clients"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(30))
    last_name: Mapped[str] = mapped_column(String(40))
    phone_no: Mapped[str] = mapped_column(String(15), unique=True)
    email: Mapped[Optional[str]] = mapped_column(String(30))

    def __repr__(self) -> str:
        return f"Client(id={self.id}, fn={self.first_name}, ln={self.last_name})"


