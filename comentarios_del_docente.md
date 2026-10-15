# Comentarios de la cátedra

Informática (TDS05) · Proyecto Integrador · UM Río Cuarto

Acá va la devolución de cada revisión semanal. Léanlo antes de seguir programando.
Primero está el alcance completo del proyecto; al final, la devolución de cada semana.

**Grupo:** Martín Ariel Meinero
**Tema:** Mendobot — Carreras y materias

---

# Alcances de este proyecto

Esto es lo que hay que entregar. Lo que no está acá, no se pide.

## Reglas comunes a todos los grupos

### Stack
- Python + **FastAPI** + Uvicorn.
- Datos en **SQLite**. Pueden usar **SQLAlchemy** (ORM, con la guía [guias/sqlalchemy_orm.md](guias/sqlalchemy_orm.md)) o **`sqlite3` con SQL directo**: las dos formas valen. **Pydantic es opcional**: el cuerpo del `POST` se puede validar con un modelo de Pydantic (`class StudentIn(BaseModel)`) o a mano en `validation.py`. Las dos formas valen.
- Repositorio en GitHub con commits de **todos** los integrantes.
- **Demo local:** la API se corre en la notebook de cada grupo con `uvicorn`. No hace falta desplegarla en la web (ver *Demo local*, abajo).

### Nombres en el código (criterio acordado con la cátedra de Inglés)

> **Actualizado el 15/10:** los nombres de tablas, columnas y rutas en inglés pasan a ser una **recomendación**. Si quedan en español, no es un error.

- **Variables, funciones y clases en inglés**: `list_students`, `get_session`, `class Student(Base)`.
- **Tablas, columnas, rutas y query params:** se recomienda que también vayan en inglés (`__tablename__ = "students"`, columna `career_id`, ruta `GET /students`), pero pueden quedar en español, como figuran en el alcance.
- Lo que sí es obligatorio: usar **el mismo nombre en todos los archivos** (`models.py`, `seed.py`, `crud.py`, `main.py`, `validation.py`). Si la tabla se llama `estudiantes` en el seed, se llama `estudiantes` en todos lados.
- **Documentación en inglés**: `README.md`, docstrings y los mensajes que devuelve la API.
- **Comentarios**: pueden estar en español mientras desarrollan, pero para la **entrega final** tienen que estar en inglés.

### Demo local (sin despliegue)

> **Actualizado el 15/10:** no se despliega a producción. La defensa es **local**, en la notebook del grupo.

`requirements.txt` debe incluir:
```
fastapi
uvicorn
python-dotenv
```
y `sqlalchemy` si lo usan.

Para levantar el proyecto desde cero (lo mismo tiene que estar en el README):
```
python -m venv venv
venv\Scripts\activate          (en Linux/Mac: source venv/bin/activate)
pip install -r requirements.txt
python seed.py
uvicorn main:app --reload
```
Y abrir http://127.0.0.1:8000/docs.

- El seed se corre **una vez, antes** de levantar el servidor. No va adentro de `main.py`.
- Antes de la defensa, prueben todo esto en la notebook con la que van a presentar.

### Base de datos
- **3 tablas**, cada una con clave primaria (`id`).
- Al menos **1 relación** entre tablas (clave foránea, ej. `equipo_id`).
- **Algunos datos de ejemplo** en cada tabla, los suficientes para ver funcionar los endpoints. No hay mínimo ni máximo. Siempre **datos ficticios**.
- Recomendación: que los datos permitan ver los filtros en acción, por ejemplo productos de varias categorías, para que `?category=` devuelva algo distinto de la lista completa.
- Un script de carga inicial `seed.py` que crea las tablas (con `create_all` o con `CREATE TABLE IF NOT EXISTS`) y carga los datos **solo si la base está vacía**. Se ejecuta antes de levantar el servidor y, si se corre dos veces, no duplica nada.
- El archivo `.db` **puede estar en el repo**. Si lo suben, que esté actualizado (el que genera el seed actual).

### Seguridad: TODOS los endpoints van protegidos

> **Actualizado el 15/10:** se **recomienda** guardar la clave en una variable de entorno en lugar de escribirla en el código. No es obligatorio; en la defensa se puede preguntar por qué conviene hacerlo.

- Todos los endpoints piden la API key en el encabezado `X-API-Key`.
- Sin clave o con clave incorrecta → **401**. Con la clave correcta → **200** y los datos.
- **Recomendado:** guardar la clave en un archivo **`.env`** que **no se sube** (va en el `.gitignore`) y leerla con `python-dotenv`. Al repo se sube un **`.env.example`** con el nombre de la variable y sin el valor. Paso a paso en [guias/variables_de_entorno.md](guias/variables_de_entorno.md). Si la dejan como constante en `security.py`, también vale.
- Los datos son todos **ficticios**: esta API no se usa para nada real.

`security.py` con la clave en el `.env` (la forma recomendada):

```python
import os

from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader

load_dotenv()
API_KEY = os.getenv("API_KEY")
header = APIKeyHeader(name="X-API-Key")


def verify_api_key(key: str = Depends(header)):
    if API_KEY is None or key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
```

Y en `main.py` se protege toda la app de una vez:

```python
app = FastAPI(dependencies=[Depends(verify_api_key)])
```

En `/docs` usá el botón **Authorize** para cargar la clave y probar.
---

## Nivel A — obligatorio (igual para todos)

Cada grupo implementa **exactamente estos 6 endpoints**, adaptados a su tema (ver *Alcance de este grupo*):

| # | Tipo | Ejemplo genérico | Qué practica |
|---|---|---|---|
| 1 | Listado con filtro | `GET /cosas?campo=valor` | Query param y filtro en la consulta |
| 2 | Detalle | `GET /cosas/{id}` | Path param, **404** si no existe |
| 3 | Relación | `GET /cosas/{id}/otras` | Cruzar dos tablas por la clave foránea |
| 4 | Segundo listado con filtro | `GET /otras?campo=valor` | Query param sobre otra tabla |
| 5 | Calculado | `GET /resumen` | Contar, sumar o agrupar (en Python o en la consulta) |
| 6 | Alta | `POST /cosas` | Recibir el cuerpo (con un modelo de Pydantic o como `dict` validado a mano), rechazar los datos inválidos con **400** o **422**, e insertar en la base |

Además, en Nivel A:
- **Errores:** 401 (sin clave), 404 (no existe), y la API no se cae si la base no está o falla una consulta (`try/except`).
- **Filtros opcionales:** si no se manda el query param, devuelve todo.
- **Seguridad (recomendado):** API key en variable de entorno (`.env`) en lugar de escrita en el código.
- **README:** qué hace la API, lista de endpoints, cómo usar la API key, cómo correrla localmente, y declaración de uso de IA si la usaron.

## Nivel B — opcional

Existe un Nivel B que suma hasta 1 punto sobre la nota final. **No se preocupen por eso todavía:** lo vemos en clase más adelante, cuando el Nivel A esté andando.

---

## Alcance de este grupo

### Grupo 1 · Mendobot — Carreras y materias
**Integrantes:** Martín Ariel Meinero

**Tablas**
- `sedes`: id, nombre, ciudad, direccion
- `carreras`: id, codigo, nombre, modalidad, duracion_anios, sede_id (FK)
- `materias`: id, nombre, anio, carrera_id (FK)

**Endpoints Nivel A**
1. `GET /carreras?modalidad=presencial`
2. `GET /carreras/{id}`
3. `GET /carreras/{id}/materias?anio=1`
4. `GET /sedes?ciudad=Rio Cuarto`
5. `GET /carreras/{id}/resumen` → cantidad de materias por año
6. `POST /materias`


---

## Fuera de alcance (para todos)

No se pide y **no suma**:
- Frontend o páginas web.
- Login de usuarios, registro, JWT.
- Bases de datos externas (PostgreSQL, MySQL, etc.).
- Docker.
- Integración con IA o con el chatbot (eso corresponde a Análisis de Sistemas).
- Pagos, facturación, envío de mails, hardware real.

## Entregables

1. Repositorio GitHub: `main.py`, script de seed, `requirements.txt`, `README.md`, commits de todos.
2. Video demo (máx. 5 min): endpoints funcionando con clave, y un pedido **sin** clave mostrando el 401.
3. Defensa oral el **miércoles 28/10**: demo en vivo desde `/docs`, en local, y preguntas sobre el código. El repositorio tiene que estar al día el **miércoles 21/10**.

---

# Devolución semanal

## 23/09

**📌 Novedad:** la base se maneja con **SQLAlchemy** (ORM) y **sin Pydantic**; las validaciones del `POST` van a mano. Hay una guía con ejemplo completo en [guias/sqlalchemy_orm.md](guias/sqlalchemy_orm.md) y el código en `guias/pokedex/`. Agreguen `sqlalchemy` a `requirements.txt`.

**Lo que hay:** `API.py` con `print("hello world?")` y el README con el tema.

**A corregir**
- El archivo de la API tiene que llamarse `main.py`, porque el comando de arranque es `gunicorn main:app`.
- `print()` no es una API. Hace falta `app = FastAPI()` y al menos un endpoint que devuelva JSON.

**Próximos pasos**
1. `main.py` con FastAPI levantando y `/docs` abriendo.
2. `seed.py` que cree las 3 tablas (`sedes`, `carreras`, `materias`) y cargue unos 10 registros de cada una.
3. Recordá la clave foránea: `materias.carrera_id` y `carreras.sede_id`.

## 24/09

**📌 Criterio de nombres.** Variables, funciones y clases en **inglés**; tablas, columnas y rutas como en el alcance; comentarios en inglés para la entrega final. Está detallado arriba en *Reglas comunes* y la guía ya lo aplica.

**Lo que hay:** renombraste `API.py` a `main.py` 👍, pero el contenido **no arranca**: falta `from fastapi import FastAPI`, y las llaves `{ ... }` que envuelven `carreras = [...]` son un error de sintaxis (una asignación no puede ir dentro de un diccionario).

**A corregir**
- `main.py` mínimo que levante:
  ```python
  from fastapi import FastAPI
  app = FastAPI()

  @app.get("/")
  def inicio():
      return {"mensaje": "Mendobot API"}
  ```
- Los datos de carreras y materias no van escritos en `main.py`: van en la base, cargados por `seed.py`. `main.py` solo consulta.
- **La base va con SQLAlchemy** (ver [guias/sqlalchemy_orm.md](guias/sqlalchemy_orm.md)): tablas como clases. Sin `sqlite3` ni SQL a mano.
- Falta `requirements.txt`.

**Próximos pasos**
1. `main.py` levantando y `/docs` abriendo.
2. `seed.py` con SQLAlchemy: `sedes`, `carreras` (con `sede_id` y `duracion_anios`) y `materias` (con `carrera_id` y `anio`), ~10 registros por tabla, carga solo si está vacía.
3. `requirements.txt` con `fastapi`, `uvicorn`, `uvicorn-worker`, `gunicorn`, `sqlalchemy`.

## 08/10

**📌 Cambio de criterio: todo en inglés.** Ahora también las **tablas, columnas, rutas y query params** van en inglés, igual que el README, los docstrings y los mensajes de la API. Reemplaza lo dicho el 24/09; está detallado arriba en *Nombres en el código*. El alcance sigue listando los nombres en español solo como referencia.

**📌 Guía nueva (opcional):** [guias/variables_de_entorno.md](guias/variables_de_entorno.md), para sacar la clave del código con un `.env`.

**Lo que hay:** sin cambios. El último commit es del **23/09**, hace más de dos semanas, y `main.py` sigue sin arrancar por los mismos dos errores que marqué el 24/09 (falta el `import` y sobran las llaves).

**⚠️ Estás muy atrasado.** Hay grupos con los seis endpoints funcionando y otros con la base ya armada. Trabajás solo, así que nadie más va a empujar el proyecto. Si estás trabado con algo puntual, decímelo en clase o por mensaje: es mejor preguntar que no subir nada.

**Próximos pasos (urgente)** — son los mismos del 24/09, con los nombres ya en inglés:
1. `main.py` mínimo que levante. Probalo con `uvicorn main:app --reload` y abrí `/docs`:
   ```python
   from fastapi import FastAPI

   app = FastAPI()

   @app.get("/")
   def home():
       return {"message": "Mendobot API"}
   ```
2. `db.py` con SQLAlchemy, siguiendo la [guía](guias/sqlalchemy_orm.md). Podés copiar `guias/pokedex/db.py` y adaptarlo. Las tres tablas, en inglés:
   - `locations`: id, name, city, address
   - `careers`: id, code, name, mode, duration_years, `location_id` (FK)
   - `subjects`: id, name, year, `career_id` (FK)
3. `seed.py` que cargue unos 10 registros por tabla, solo si la base está vacía (sección 9 de la guía).
4. `requirements.txt` con `fastapi`, `uvicorn`, `uvicorn-worker`, `gunicorn`, `sqlalchemy`.
5. Los dos primeros endpoints: `GET /careers?mode=` y `GET /careers/{id}` con 404.

Subí cada paso apenas funcione, aunque sea chico. Un commit por día vale más que todo junto al final.

## 15/10

**📌 Cambios en las reglas** (están arriba, en *Reglas comunes*):
- **SQLAlchemy es opcional:** también vale `sqlite3` con SQL directo.
- **No hay que desplegar.** La defensa es **local**, en tu notebook, el **miércoles 28/10**. El repo tiene que estar al día el **miércoles 21/10**.
- **Recomendado:** la API key en una variable de entorno (`.env`) en lugar de escrita en el código. No es obligatorio, pero en la defensa se puede preguntar dónde está la clave y por qué conviene sacarla del código.

**Lo que hay:** sin cambios. El último commit es del **23/09** y `main.py` sigue sin arrancar.

**⚠️ Quedan 6 días para la entrega.** Con lo que hay hoy, el proyecto no se puede defender. Si querés presentarlo, escribime **esta semana** para ver qué es posible llegar a mostrar.

**El mínimo para tener algo que defender**, en este orden:
1. `main.py` que levante con `uvicorn main:app --reload`, con el ejemplo del 08/10.
2. `seed.py` que cree las tres tablas (`locations`, `careers`, `subjects`) con `sqlite3` y cargue algunos datos en cada una. Con `sqlite3` es más corto que con SQLAlchemy.
3. `crud.py` con dos funciones y sus endpoints: `GET /careers?mode=` (listado con filtro) y `GET /careers/{id}` (detalle con 404).
4. `security.py` con la API key, y probar que sin clave da 401. Si llegás, leela de un `.env` en vez de escribirla en el código.
5. Un endpoint que calcule algo: `GET /careers/{id}/summary`, con la cantidad de materias por año.
6. `requirements.txt` y un README que diga cómo correrlo. Hay guías para las dos cosas en `guias/`.
