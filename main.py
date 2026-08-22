import os
from pathlib import Path

from fastapi import FastAPI, Depends

import uuid
import bcrypt

# ORM libs
from sqlalchemy import select
from sqlalchemy.orm import Session


def _load_dotenv(dotenv_path: Path) -> None:
    if not dotenv_path.is_file():
        return

    for line in dotenv_path.read_text().splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if "=" not in stripped:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        if not key or key in os.environ:
            continue

        value = value.strip().strip('"').strip("'")
        os.environ[key] = value


_load_dotenv(Path(__file__).resolve().parent / ".env")

from routers.auth import authEngine, AuthGetDB
from routers.weight import weightEngine, WeightGetDB

from models.user import User, UserBase
from models.weight import Weight, WeightBase


import cppmethods # my cpp functions

app = FastAPI()

UserBase.metadata.create_all(authEngine)
WeightBase.metadata.create_all(weightEngine)


@app.get("/ping")
def Ping():
    return {"ping": "pong!"}

@app.get("/uuid")
def GetUuid():
    id = uuid.uuid4()
    return {"uuid": id}


# Hashing functions
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

# cppmethods example
@app.get("/add")
def Add(a: int = 1, b: int = 1):
    return {"output": cppmethods.add(a, b)}


# Authentication
@app.get("/users")
def GetUsers(db: Session = Depends(AuthGetDB)):
    users = db.query(User).all()
    return users

@app.get("/user/exists")
def GetUserByName(name: str, db: Session = Depends(AuthGetDB)):
    statement = select(User).where(User.username == name)
    try:
        user = db.execute(statement).scalar_one_or_none()
        return {"user": user}
    except Exception as ex:
        return {"error": str(ex)}
    
@app.get("/authdb/test")
def DbTest(db: Session = Depends(AuthGetDB)):
    statement = select(User).limit(1)

    try:
        user = db.execute(statement).scalar_one_or_none()
        return {"orm": "ok", "user_found": user is not None}
    except Exception as exc:
        return {"orm": "error", "detail": str(exc)}


@app.get("/auth/server")
def ServerAuth(user: str = "", password: str = "", db: Session = Depends(AuthGetDB)):
    # get stored hash from server

    statement = select(User).where(User.username == user).limit(1)

    try:
        user = db.execute(statement).scalar_one_or_none()
        print("🚀 ~ ServerAuth ~ user:", user)
    except Exception as ex:
        return {"user": user, "serverAuth": False, "error": str(ex)}
    
    output = CheckBcrypt(password, user.password_hash)
    
    print("🚀 ~ ServerAuth ~ output:", output)

    return {"user": user.username, "serverAuth": output.get("valid", False)}


# Weight
@app.post("/weight/log")
def weightLog(weight_lb: float = 0.0, db: Session = Depends(WeightGetDB)):
    if weight_lb <= 0.0:
        return {"input weight_lb": weight_lb, "error": "Weight must be greater than 0"}

    statement = Weight(weight_lb=weight_lb)
    
    try:
        db.add(statement)
        db.commit()
        db.refresh(statement)
    except Exception as ex:
        try:
            db.rollback()
        except Exception:
            pass
        return {"input weight_lb": weight_lb, "error": str(ex)}

    return {"input weight_lb": weight_lb, "output": weight_lb, "id": getattr(statement, "id", None), "timestamp": getattr(statement, "timestamp", None)}


@app.get("/url/encode")
def URLEncode(input: str = ""):
    pass

@app.get("/url/decode")
def URLDecode(input: str = ""):
    pass

@app.get("/url/normalizer")
def URLNormalizer(input: str = ""):
    pass


### Webhooks ###
@app.post("/webhook/deploy")
def DeployMicroservices(service: str = "", bearerToken: str = ""):
    validServices = ["recipemanager", "microservices", "controlpanel", "ogpt", "strava"]

    if service not in validServices:
        return {"error": f"Invalid service: {service}"}

    if not bearerToken:
        return {"error": "Missing bearer token"}

    if bearerToken != os.environ.get("WEBHOOK_BEARER_TOKEN", ""):
        return {"error": "Invalid bearer token"}

    

    return {"services": service, "success": 1}