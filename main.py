from fastapi import FastAPI

import uuid
import os

import cppmethods # my cpp functions

ENV = os.getenv("ENV", "dev")

if ENV == "dev":
    BASE_URL = ""
else:
    BASE_URL = "/micro"

app = FastAPI(
    root_path=BASE_URL
)

@app.get("/uuid")
def GetUuid():
    id = uuid.uuid4()
    return {"uuid": id}

@app.get("/openssl/sha256sum")
def SHA256Sum(input: str = ""):
    output = cppmethods.sha256sum(input)

    return {"input": input, "output": output}

@app.get("/openssl/keypairgen")
def GenerateKeyPair(usefulText: str = "USEFUL_NOTE"):
    return {"pub.key": "-1", "key.pem": "-1"}

@app.get("/add")
def Add(a: int = 1, b: int = 1):
    return {"result": cppmethods.add(a, b)}