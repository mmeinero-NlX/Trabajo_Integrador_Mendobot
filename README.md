# Mendobot API

REST API that serves the data for MendoBot, a chatbot for future students of
Universidad de Mendoza (Río Cuarto). It provides careers, their subjects and
the university locations. Built with FastAPI, SQLAlchemy and SQLite for the
Informática course of the Software Development Technician program
(Tecnicatura en Desarrollo de Software).

## Author

- Martín Ariel Meinero

## Requirements

- Python 3.11 or newer
- Git

## How to run it

1. Clone the repository and enter the folder:

   ```
   git clone https://github.com/mmeinero-NlX/Trabajo_Integrador_Mendobot.git
   cd Trabajo_Integrador_Mendobot
   ```

2. Create and activate a virtual environment:

   ```
   python -m venv venv
   venv\Scripts\activate
   ```

   On Linux or Mac: `source venv/bin/activate`

3. Install the dependencies:

   ```
   pip install -r requirements.txt
   ```

4. Create the `.env` file from the example:

   ```
   copy .env.example .env
   ```

   On Linux or Mac: `cp .env.example .env`

   Then open `.env` and write: `API_KEY=test-key-2026`

5. Create the database and load the sample data (only once):

   ```
   python seed.py
   ```

6. Start the server:

   ```
   uvicorn main:app --reload
   ```

7. Open http://127.0.0.1:8000/docs

## How to use it

Every endpoint requires the API key in the `X-API-Key` header.
In `/docs`, click **Authorize** and paste the key: `test-key-2026`.

| Method | Path                          | Description                                        |
|--------|-------------------------------|----------------------------------------------------|
| GET    | /careers?mode=presencial      | List careers, optionally filtered by mode          |
| GET    | /careers/{id}                 | Get one career                                     |
| GET    | /careers/{id}/subjects?year=1 | List the subjects of a career, optionally by year  |
| GET    | /locations?city=Mendoza       | List locations, optionally filtered by city        |
| GET    | /careers/{id}/summary         | Count the subjects of a career by year             |
| POST   | /subjects                     | Create a subject                                   |

Example:

```
curl -H "X-API-Key: test-key-2026" http://127.0.0.1:8000/careers/2/summary
```

```json
{"career_id": 2, "total_subjects": 36, "subjects_by_year": {"1": 7, "2": 6, "3": 6, "4": 6, "5": 11}}
```

To create a subject, send a JSON body to `POST /subjects`:

```json
{"name": "Inglés III", "year": 3, "career_id": 1}
```

Rules: `name` cannot be empty (max 100 characters), `year` must be an integer
between 1 and 5 and cannot be greater than the career duration, and
`career_id` must exist.

Errors:

- `401` without a valid key
- `404` if the career does not exist
- `400` if the data sent is invalid
- `500` if the database is not available

## Database

Three tables: `locations`, `careers` (with `location_id`) and `subjects`
(with `career_id`). A location has many careers and a career has many subjects.
All the data is sample data, loaded by `seed.py`.

## Use of AI

I used an AI assistant (Claude) to go through the course material faster
(FastAPI, API keys, files, etc.), to get code suggestions based on the Pokédex
example code, and also to find errors. Then I wrote, tested and reviewed every
part of the code myself.