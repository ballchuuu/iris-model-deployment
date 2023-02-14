import bentoml
import numpy as np
from bentoml.io import NumpyNdarray
from config import settings

runner = bentoml.sklearn.get(f"{settings.bento_model_name}:latest").to_runner()
svc = bentoml.Service(settings.bento_model_name, runners=[runner])

@svc.api(input=NumpyNdarray(), output=NumpyNdarray())
def classify(input_series: np.ndarray) -> np.ndarray:
    result = runner.predict.run(input_series)
    return result
