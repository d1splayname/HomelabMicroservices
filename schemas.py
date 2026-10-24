from pydantic import BaseModel

class WeightLogRequest(BaseModel):
    weight_lb: float


class GasLogRequest(BaseModel):
    price: float


class ClimateUpdateRequest(BaseModel):
    dataType: str
    data: float
