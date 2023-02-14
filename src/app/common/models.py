from pydantic import BaseModel

###
# Common Utilies Models
###
class SimpleMessageResponse(BaseModel):
    message: str