from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.exc import IntegrityError, OperationalError

import crud
from security import verify_api_key

app = FastAPI(title="Mendobot API", dependencies=[Depends(verify_api_key)])


# 1) List careers, optionally filtered by mode
@app.get("/careers")
def list_careers(mode: str | None = None):
    try:
        return crud.list_careers(mode)
    except OperationalError:
        raise HTTPException(status_code=500, detail="Database error")


# 2) Get one career (404 if it does not exist)
@app.get("/careers/{career_id}")
def get_career(career_id: int):
    try:
        career = crud.get_career(career_id)
        if career is None:
            raise HTTPException(status_code=404, detail="Career not found")
        return career
    except OperationalError:
        raise HTTPException(status_code=500, detail="Database error")


# 3) List the subjects of a career, optionally filtered by year
@app.get("/careers/{career_id}/subjects")
def list_career_subjects(career_id: int, year: int | None = None):
    try:
        if crud.get_career(career_id) is None:
            raise HTTPException(status_code=404, detail="Career not found")
        return crud.list_career_subjects(career_id, year)
    except OperationalError:
        raise HTTPException(status_code=500, detail="Database error")


# 4) List locations, optionally filtered by city
@app.get("/locations")
def list_locations(city: str | None = None):
    try:
        return crud.list_locations(city)
    except OperationalError:
        raise HTTPException(status_code=500, detail="Database error")


# 5) Count the subjects of a career by year
@app.get("/careers/{career_id}/summary")
def career_summary(career_id: int):
    try:
        if crud.get_career(career_id) is None:
            raise HTTPException(status_code=404, detail="Career not found")
        return crud.career_summary(career_id)
    except OperationalError:
        raise HTTPException(status_code=500, detail="Database error")


# 6) Create a subject (400 if the data is invalid)
@app.post("/subjects", status_code=201)
def create_subject(data: dict):
    try:
        return crud.create_subject(data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except IntegrityError:
        raise HTTPException(status_code=400, detail="career_id does not exist")
    except OperationalError:
        raise HTTPException(status_code=500, detail="Database error")