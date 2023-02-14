router_prefix = "/iris"

class TestIrisModelEndpoint:
    def test_success_endpoint(self, auth_client):
        response = auth_client.post(
            f"{router_prefix}/predict",
            json={
                "SepalLengthCm": 4.4,
                "SepalWidthCm": 3.2,
                "PetalLengthCm": 1.3,
                "PetalWidthCm": 0.2
            }
        )
        assert response.status_code == 200

    def test_wrong_input(self, auth_client):
        response = auth_client.post(
            f"{router_prefix}/predict",
            json={
                "test": 0
            }
        )
        assert response.status_code == 422

    def test_wrong_endpoint(self, auth_client):
        response = auth_client.post(
            f"{router_prefix}/test",
            json={
                "SepalLengthCm": 4.4,
                "SepalWidthCm": 3.2,
                "PetalLengthCm": 1.3,
                "PetalWidthCm": 0.2
            }
        )
        assert response.status_code == 404
