from fastapi import FastAPI

import uuid
import os

import cppmethods # my cpp functions

app = FastAPI()

@app.get("/uuid")
def GetUuid():
    id = uuid.uuid4()
    return {"uuid": id}

@app.get("/hash/sha256sum")
def SHA256Sum(input: str = ""):
    output = cppmethods.sha256sum(input)

    return {"input": input, "output": output}

@app.get("/hash/bcrypt")
def Bcrypt(input: str = ""):
    output = cppmethods.bcrypt(input)

    return {"input": input, "output": output}

@app.get("/add")
def Add(a: int = 1, b: int = 1):
    return {"result": cppmethods.add(a, b)}