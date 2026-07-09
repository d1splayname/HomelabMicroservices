from fastapi import FastAPI

import uuid

BASE_URL = "/micro"

app = FastAPI(
    root_path=BASE_URL
)

@app.get("/uuid")
def GetUuid():
    id = uuid.uuid4()
    return {"uuid": id}