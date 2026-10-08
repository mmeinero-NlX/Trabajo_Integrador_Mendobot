from fastapi import FastAPI, HTTPException
from datos import carreras

app = FastAPI()
def listar():
    return carreras