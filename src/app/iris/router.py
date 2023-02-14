from app.core.logger import logger
from app.iris.models import InputIris
from app.iris.models import IrisInfoLog
from app.iris.models import OutputIris
from app.iris.utils import get_iris_prediction
from fastapi import APIRouter

router = APIRouter()

@router.post("/predict", response_model=OutputIris)
async def iris_endpoint(
    param: InputIris
):

    response = await get_iris_prediction(param)

    logger.info(
        IrisInfoLog(
            param=param,
            response=response
        ).json()
    )
    return response
