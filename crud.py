from sqlalchemy import select
from models import get_session, Career, Subject


def list_careers(mode: str | None = None) -> list[dict]:
    with get_session() as s:
        query = select(Career)
        if mode is not None:
            query = query.where(Career.mode == mode)
        return [career.to_dict() for career in s.scalars(query)]

def get_career(career_id: int) -> dict | None:
    with get_session() as s:
        career = s.get(Career, career_id)
        return career.to_dict() if career else None

def list_career_subjects(career_id: int, year: int | None = None) -> list[dict]:
    with get_session() as s:
        query = select(Subject).where(Subject.career_id == career_id)
        if year is not None:
            query = query.where(Subject.year == year)
        return [subject.to_dict() for subject in s.scalars(query)]