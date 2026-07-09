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

@app.get("/openssl/SHA256sum")
def SHA256Sum(input="123"):
    result = input

    return {"SHA256sum": result}

@app.get("/openssl/keypairgen")
def GenerateKeyPair(input="123"):
    return {"pub.key": "-1", "key.pem": "-1"}