from fastapi import FastAPI

import uuid

# import my cpp functions
import cppmethods

BASE_URL = "/micro"

app = FastAPI(
    root_path=BASE_URL
)

@app.get("/uuid")
def GetUuid():
    id = uuid.uuid4()
    return {"uuid": id}

@app.get("/openssl/sha256sum")
def SHA256Sum(input: str = "123"):
    result = input

    return {"sha256sum": cppmethods.sha256sum(input)}

@app.get("/openssl/keypairgen")
def GenerateKeyPair(input="123"):
    return {"pub.key": "-1", "key.pem": "-1"}