from fastapi import FastAPI

import uuid

BASE_URL = "/micro"

app = FastAPI(
    root_path="/micro"
    # docs_url=f"{BASE_URL}/docs",
    # redoc_url=f"{BASE_URL}/redoc",
    # openapi_url=f"{BASE_URL}/openapi.json"
)

@app.get("/uuid")
def GetUuid():
    id = uuid.uuid4()
    return id