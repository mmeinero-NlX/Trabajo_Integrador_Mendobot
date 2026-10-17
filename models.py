from sqlalchemy import create_engine, event, ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session

DB_FILE = "mendobot.db"

engine = create_engine(f"sqlite:///{DB_FILE}")


@event.listens_for(engine, "connect")
def enable_foreign_keys(con, _):
    con.execute("PRAGMA foreign_keys = ON")


class Base(DeclarativeBase):
    pass


class Location(Base):
    __tablename__ = "locations"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    city: Mapped[str] = mapped_column(String(50))
    address: Mapped[str] = mapped_column(String(100))

    def to_dict(self) -> dict:
        return {"id": self.id, "name": self.name, "city": self.city, "address": self.address}


class Career(Base):
    __tablename__ = "careers"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(10), unique=True)
    name: Mapped[str] = mapped_column(String(50))
    mode: Mapped[str] = mapped_column(String(20))
    duration_years: Mapped[int]
    location_id: Mapped[int] = mapped_column(ForeignKey("locations.id"))

    location: Mapped[Location] = relationship()


    def to_dict(self) -> dict:
        return {"id": self.id, "code": self.code, "name": self.name, "mode": self.mode, "duration_years": self.duration_years, "location_id": self.location_id}


class Subject(Base):
    __tablename__ = "subjects"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    year: Mapped[int]
    career_id: Mapped[int] = mapped_column(ForeignKey("careers.id"))

    career: Mapped[Career] = relationship()

    def to_dict(self) -> dict:
        return {"id": self.id, "name": self.name, "year": self.year, "career_id": self.career_id}


def create_tables():
    Base.metadata.create_all(engine)


def get_session() -> Session:
    return Session(engine)