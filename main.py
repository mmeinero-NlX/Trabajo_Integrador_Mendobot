from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.exc import OperationalError

import crud
from security import verify_api_key

app = FastAPI(title="Mendobot API", dependencies=[Depends(verify_api_key)])


# 1) Listar carreras, con filtro opcional por modalidad
@app.get("/careers")
def list_careers(mode: str | None = None):
    try:
        return crud.list_careers(mode)
    except OperationalError:
        raise HTTPException(status_code=500, detail="Database error")


# 2) Detalle de una carrera (404 si no existe)
@app.get("/careers/{career_id}")
def get_career(career_id: int):
    career = crud.get_career(career_id)
    if career is None:
        raise HTTPException(status_code=404, detail="Career not found")
    return career


# 3) Materias de una carrera, con filtro opcional por año
@app.get("/careers/{career_id}/subjects")
def list_career_subjects(career_id: int, year: int | None = None):
    if crud.get_career(career_id) is None:
        raise HTTPException(status_code=404, detail="Career not found")
    return crud.list_career_subjects(career_id, year)


# 4) PENDIENTE


# 5) Cantidad de materias por año de una carrera
@app.get("/careers/{career_id}/summary")
def career_summary(career_id: int):
    if crud.get_career(career_id) is None:
        raise HTTPException(status_code=404, detail="Career not found")
    return crud.career_summary(career_id)


# 6) PENDIENTE