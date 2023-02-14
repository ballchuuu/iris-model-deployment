import random

from locust import HttpUser
from locust import task

class QuickstartUser(HttpUser):
    @task
    def loadtest_predict(self):
        """
        Function swarms the /predict endpoint with random feature values
        """
        data = {
            'SepalLengthCm': random.uniform(0.1, 9.0),
            'SepalWidthCm': random.uniform(0.1, 9.0),
            'PetalLengthCm': random.uniform(0.1, 9.0),
            'PetalWidthCm': random.uniform(0.1, 9.0)
        }
        with self.client.post(
            "/iris/predict",
            json=data,
            catch_response=True
        ) as resp:
            result = resp.json()

            # check if the result returns error
            if result["output"] not in [
                "Iris-setosa", "Iris-versicolor", "Iris-virginica"
            ]:
                resp.failure("Got wrong response")
