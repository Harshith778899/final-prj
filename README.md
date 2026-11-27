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

## GitHub Actions deployment

The `API CI/CD` workflow runs syntax and endpoint checks for pushes and pull
requests. To trigger Render deployments on pushes to `main`, create a deploy
hook for the Render service and add its URL to the GitHub repository as the
`RENDER_DEPLOY_HOOK_URL` Actions secret. Until configured, CI will pass and
the deploy step will emit a warning. Do not commit the hook URL.
