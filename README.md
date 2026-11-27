# Duplicate-Safe Incremental Merge Platform

FastAPI backend for validating and processing incremental CSV merges.

## Run locally

From the project root in PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r backend\requirements-api.txt
.\.venv\Scripts\python.exe -m uvicorn app.main:app --app-dir backend --reload
```

The API is available at `http://127.0.0.1:8000`; interactive docs are at
`http://127.0.0.1:8000/docs`.

The merge endpoint optionally stores run details in MySQL. Configure
`DB_HOST`, `DB_USER`, `DB_PASSWORD`, and `DB_NAME` in the environment for
database persistence. Do not commit credentials or data files.

## Deploy on Render

Create a Render Blueprint from this repository and select `render.yaml`.
The included service runs the API without database persistence; configure
the `DB_*` environment variables in Render if MySQL is available.
