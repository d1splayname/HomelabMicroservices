from fastapi import FastAPI, Depends
from dotenv import load_dotenv

import os
import subprocess
import uuid
import bcrypt
import uvicorn
import sys

import cppmethods # my cpp functions

# ORM libs
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from routers.weight import weightEngine, WeightGetDB
from models.weight import Weight, WeightBase

from routers.gas import gasEngine, GasGetDB
from models.gas import Gas, GasBase

from routers.climate import climateEngine, ClimateGetDB
from models.climate import Climate, ClimateBase

from helper import CToF, FToC


load_dotenv()
app = FastAPI()

JOSHUAHP_MAC_ADDR = os.getenv("JOSHUAHP_MAC_ADDR")

WeightBase.metadata.create_all(weightEngine)
GasBase.metadata.create_all(gasEngine)
ClimateBase.metadata.create_all(climateEngine)


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
        return {"error": "Invalid hash length"}, 400

    return {"valid": bcrypt.checkpw(encodedPass, encodedHash)}

# cppmethods example
@app.get("/add")
def Add(a: int = 1, b: int = 1):
    return {"output": cppmethods.add(a, b)}


# Weight
@app.post("/log/weight")
def weightLog(weight_lb: float, db: Session = Depends(WeightGetDB)):
    if weight_lb <= 0.0:
        return {"input weight_lb": weight_lb, "error": "Weight must be greater than 0"}, 400

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
        return {"input weight_lb": weight_lb, "error": str(ex)}, 500

    return {"input weight_lb": weight_lb, "output": weight_lb, "id": getattr(statement, "id", None), "timestamp": getattr(statement, "timestamp", None)}

# Gas
@app.post("/log/gas")
def GasLog(price: float, db: Session = Depends(GasGetDB)):
    if price <= 0.0:
        return {"input": price, "error": "Price must be greater than 0"}, 400

    # sanity check:
    # gas shouldn't be more than $10 or else that would be insane
    while price > 10:
        price /= 10

    price = round(price, 2)

    statement = Gas(price=price)

    try:
        db.add(statement)
        db.commit()
        db.refresh(statement)
    except Exception as ex:
        try:
            db.rollback()
        except Exception:
            pass

        return {"input price": price, "error": str(ex)}, 500

    return {"input": price, "success": True}


# Climate control
@app.post("/climate")
def GetClimate(dataType: str, data: float, db: Session = Depends(ClimateGetDB)):
    if dataType not in ["temperature", "humidity"]:
        return {"input": dataType, "error": "Invalid dataType"}, 400

    if not data:
        return {"input": data, "error": "Data must be provided"}, 400

    if data <= 0.0:
        return {"input": data, "error": "Data must be greater than 0"}, 400
    
    statement = db.query(Climate).filter(Climate.type == dataType).first()

    if statement:
        statement.data = data
        statement.timestamp = func.current_timestamp()
        db.commit()
    else:
        statement = Climate(type=dataType, data=data)
        db.add(statement)
        db.commit()

    return {"success": True}

@app.get("/climate")
def GetClimate(dataType: str, db: Session = Depends(ClimateGetDB)):
    if dataType not in ["temperature", "humidity"]:
        return {"input": dataType, "error": "Invalid dataType"}, 400

    statement = select(Climate).where(Climate.type == dataType).order_by(Climate.timestamp.desc()).limit(1)
    result = db.scalars(statement).first()

    if result is None:
        return {"dataType": dataType, "data": None, "timestamp": None}
    
    return {"dataType": dataType, "data": result.data, "timestamp": result.timestamp}


@app.get("/url/encode")
def URLEncode(input: str = ""):
    pass

@app.get("/url/decode")
def URLDecode(input: str = ""):
    pass

@app.get("/url/normalizer")
def URLNormalizer(input: str = ""):
    pass

@app.get("/wake/joshuahp")
def WakeUpJoshuaHP():
    subprocess.call(["wakeonlan", JOSHUAHP_MAC_ADDR])

if __name__ == "__main__":
    _host = "localhost"
    _port: int = 3002

    _reload: bool = False

    if len(sys.argv) > 1:
        if sys.argv[1] == "help":
            print("Usage: python {sys.argv[0]} [OPTIONS]")
            print(" dev     run in development mode")
            print(" help    show this message")

            exit(0)
        if sys.argv[1] == "dev":
            print("Microservices: dev mode")

            _port = 3999

            _reload = True

    uvicorn.run("main:app", host=_host, port=_port, reload=_reload)