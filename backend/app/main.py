from fastapi import FastAPI
from app.routes.merge_routes import router as merge_router

app = FastAPI(
    title="Duplicate Safe Incremental Merge Platform",
    description="Backend API for Duplicate-Safe Incremental Merge Diagnostics and Repair Platform",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "status": "success",
        "message": "Welcome to Duplicate Safe Incremental Merge Platform API"
    }


app.include_router(merge_router)