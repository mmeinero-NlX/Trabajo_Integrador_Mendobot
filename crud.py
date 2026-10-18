from sqlalchemy import select
from models import get_session, Location, Career, Subject
from validation import validate_subject

# 1) Lista las carreras. Si viene "mode", filtra por modalidad.
def list_careers(mode: str | None = None) -> list[dict]:
    with get_session() as s:
        query = select(Career)
        if mode is not None:
            query = query.where(Career.mode == mode)
        return [career.to_dict() for career in s.scalars(query)]


# 2) Busca una carrera por su id. Devuelve None si no existe.
def get_career(career_id: int) -> dict | None:
    with get_session() as s:
        career = s.get(Career, career_id)
        return career.to_dict() if career else None


# 3) Lista las materias de una carrera (cruza tablas por la FK career_id).
def list_career_subjects(career_id: int, year: int | None = None) -> list[dict]:
    with get_session() as s:
        query = select(Subject).where(Subject.career_id == career_id)
        if year is not None:
            query = query.where(Subject.year == year)
        return [subject.to_dict() for subject in s.scalars(query)]


# 4) Lista las sedes. Si viene "city", filtra por ciudad.
def list_locations(city: str | None = None) -> list[dict]:
    with get_session() as s:
        query = select(Location)
        if city is not None:
            query = query.where(Location.city == city)
        return [location.to_dict() for location in s.scalars(query)]


# 5) Cuenta las materias de una carrera agrupadas por año.
def career_summary(career_id: int) -> dict:
    with get_session() as s:
        query = select(Subject).where(Subject.career_id == career_id)
        by_year = {}
        for subject in s.scalars(query):
            if subject.year in by_year:
                by_year[subject.year] += 1
            else:
                by_year[subject.year] = 1
        return {
            "career_id": career_id,
            "total_subjects": sum(by_year.values()),
            "subjects_by_year": by_year,
        }


# 6) Valida los datos y crea una materia nueva.
def create_subject(data: dict) -> dict:
    clean = validate_subject(data)
    with get_session() as s:
        subject = Subject(**clean)
        s.add(subject)
        s.commit()
        return subject.to_dict()