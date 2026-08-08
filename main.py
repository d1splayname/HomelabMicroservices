from fastapi import FastAPI

import uuid
import bcrypt

import cppmethods # my cpp functions

app = FastAPI()

@app.get("/uuid")
def GetUuid():
    id = uuid.uuid4()
    return {"uuid": id}

@app.get("/hash/sha256sum")
def SHA256Sum(input: str = ""):
    output = cppmethods.sha256sum(input)

    return {"input": input, "sha256sum": output}

@app.get("/hash/bcrypt")
def Bcrypt(input: str = ""):
    encodedPass = input.encode() # default encoding is utf-8

    output = bcrypt.hashpw(encodedPass, bcrypt.gensalt())

    return {"input": input, "bcrypt": output}

@app.get("/hash/checkBcrypt")
def CheckBcrypt(input: str = "", storedHash: str = ""):
    encodedPass = input.encode()
    encodedHash = storedHash.encode()

    if len(storedHash) != 60:
        return {"error": "Invalid hash length"}

    return {"valid": bcrypt.checkpw(encodedPass, encodedHash)}

@app.get("/add")
def Add(a: int = 1, b: int = 1):
    return {"output": cppmethods.add(a, b)}


# Server helper functions
def _QueryServerAuth(command, params):
    pass

def _QueryServerWeight(command, params):
    pass


@app.get("/url/encode")
def URLEncode(input: str = ""):
    pass

@app.get("/url/decode")
def URLDecode(input: str = ""):
    pass

@app.get("/url/normalizer")
def URLNormalizer(input: str = ""):
    pass