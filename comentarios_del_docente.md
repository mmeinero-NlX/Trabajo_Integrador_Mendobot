# Comentarios de la cátedra

Informática (TDS05) · Proyecto Integrador · UM Río Cuarto

Acá va la devolución de cada revisión semanal. Léanlo antes de seguir programando.
El alcance completo del grupo está en el documento de alcances.

**Grupo:** Martín Ariel Meinero
**Tema:** Mendobot — Carreras y materias

---

## 23/09

**Lo que hay:** `API.py` con `print("hello world?")` y el README con el tema.

**A corregir**
- El archivo de la API tiene que llamarse `main.py`, porque el comando de arranque es `gunicorn main:app`.
- `print()` no es una API. Hace falta `app = FastAPI()` y al menos un endpoint que devuelva JSON.

**Próximos pasos**
1. `main.py` con FastAPI levantando y `/docs` abriendo.
2. `seed.py` que cree las 3 tablas (`sedes`, `carreras`, `materias`) y cargue unos 10 registros de cada una.
3. Recordá la clave foránea: `materias.carrera_id` y `carreras.sede_id`.

**Endpoints a entregar (Nivel A)**
- [ ] `GET /carreras?modalidad=presencial`
- [ ] `GET /carreras/{id}` (404 si no existe)
- [ ] `GET /carreras/{id}/materias?anio=1`
- [ ] `GET /sedes?ciudad=Rio Cuarto`
- [ ] `GET /carreras/{id}/resumen` (materias por año)
- [ ] `POST /materias`
- [ ] Todos protegidos con `X-API-Key` (clave como constante en `main.py`)
