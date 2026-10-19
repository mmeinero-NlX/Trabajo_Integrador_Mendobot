from sqlalchemy import select
from models import get_session, Location, Career, Subject
from validation import validate_subject


# 1) Lists careers. If "mode" is given, filters by mode.
def list_careers(mode: str | None = None) -> list[dict]:
    with get_session() as s:
        query = select(Career)
        if mode is not None:
            query = query.where(Career.mode == mode)
        return [career.to_dict() for career in s.scalars(query)]


# 2) Finds a career by its id. Returns None if it does not exist.
def get_career(career_id: int) -> dict | None:
    with get_session() as s:
        career = s.get(Career, career_id)
        return career.to_dict() if career else None


# 3) Lists the subjects of a career (joins tables through the career_id FK).
def list_career_subjects(career_id: int, year: int | None = None) -> list[dict]:
    with get_session() as s:
        query = select(Subject).where(Subject.career_id == career_id)
        if year is not None:
            query = query.where(Subject.year == year)
        return [subject.to_dict() for subject in s.scalars(query)]


# 4) Lists locations. If "city" is given, filters by city.
def list_locations(city: str | None = None) -> list[dict]:
    with get_session() as s:
        query = select(Location)
        if city is not None:
            query = query.where(Location.city == city)
        return [location.to_dict() for location in s.scalars(query)]


# 5) Counts the subjects of a career grouped by year.
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


# 6) Validates the data, checks the career and creates a new subject.
def create_subject(data: dict) -> dict:
    clean = validate_subject(data)
    with get_session() as s:
        career = s.get(Career, clean["career_id"])
        if career is None:
            raise ValueError("career_id does not exist")
        if clean["year"] > career.duration_years:
            raise ValueError(f"year cannot be greater than {career.duration_years} for this career")
        subject = Subject(**clean)
        s.add(subject)
        s.commit()
        return subject.to_dict()