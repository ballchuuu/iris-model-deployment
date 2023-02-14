from pydantic import BaseModel

###
# Iris model input
###
class InputIris(BaseModel):
    SepalLengthCm: float
    SepalWidthCm: float
    PetalLengthCm: float
    PetalWidthCm: float

###
# Iris model output
###
class OutputIris(BaseModel):
    output: str
    model_name: str

###
# Logging
###
class IrisInfoLog(BaseModel):
    param: InputIris
    response: OutputIris

class IrisErrorLog(BaseModel):
    param: InputIris
    error_msg: str
