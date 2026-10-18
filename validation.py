# Validaciones a mano. Reciben un dict, lo revisan y devuelven uno limpio.

def validate_subject(data: dict) -> dict:
    name = data.get("name")
    if not isinstance(name, str) or not name.strip():
        raise ValueError("name is required and cannot be empty")
    if len(name) > 100:
        raise ValueError("name cannot be longer than 100 characters")

    year = data.get("year")
    if not isinstance(year, int) or isinstance(year, bool):
        raise ValueError("year is required and must be an integer")
    if not 1 <= year <= 5:
        raise ValueError("year must be between 1 and 5")

    career_id = data.get("career_id")
    if not isinstance(career_id, int) or isinstance(career_id, bool):
        raise ValueError("career_id is required and must be an integer")

    return {"name": name.strip(), "year": year, "career_id": career_id}