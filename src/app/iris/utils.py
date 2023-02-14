import json

from app.core.config import settings
from app.core.logger import logger
from app.core.store import store
from app.iris.models import InputIris
from app.iris.models import IrisErrorLog
from app.iris.models import OutputIris

async def get_iris_prediction(input: InputIris) -> OutputIris:
    data = list(dict(input).values())

    try:
        async with store.bento_client.session.post(
            settings.bento_server,
            data=json.dumps([data])
        ) as resp:
            data = await resp.json()

            if resp.status != 200 or data is None:
                return OutputIris(
                    output="Error in prediction endpoint",
                    model_name=settings.pickle_model_name
                )

            return OutputIris(
                output=data[0],
                model_name=settings.pickle_model_name
            )

    except Exception as e:
        logger.info(IrisErrorLog(param=input, error_msg=str(e)).json())

        return OutputIris(
            output="Error in prediction endpoint",
            model_name=settings.pickle_model_name
        )
