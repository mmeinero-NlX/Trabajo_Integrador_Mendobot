from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.exc import OperationalError 

import crud
from security import verify_api_key

app = FastAPI(title="Mendobot API", dependencies=[Depends(verify_api_key)])


@app.get("/careers")
def list_careers(mode: str | None = None):
    try:
        return crud.list_careers(mode)
    except OperationalError:
        raise HTTPException(500, "Database error")

@app.get("/careers/{career_id}")
def get_career(career_id: int):
    career = crud.get_career(career_id)
    if career is None:
        raise HTTPException(status_code=404, detail="Career not found")
    return career

@app.get("/careers/{career_id}/subjects")
def list_career_subjects(career_id: int, year: int | None = None):
    if crud.get_career(career_id) is None:
        raise HTTPException(status_code=404, detail="Career not found")
    return crud.list_career_subjects(career_id, year)