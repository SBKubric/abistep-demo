from fastapi import FastAPI
from .interfaces.routes import router

app = FastAPI(
    title="User Balance Management API",
    description="A REST API for managing users and money transfers",
    version="1.0.0"
)

app.include_router(router)

@app.get("/")
async def root():
    return {"message": "User Balance Management API is running"}