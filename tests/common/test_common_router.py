class TestSimpleEndpoints:
    def test_root_path(self, auth_client):
        response = auth_client.get(
            "/",
        )

        assert response.status_code == 200

    def test_health_path(self, auth_client):
        response = auth_client.get(
            "/healthz",
        )

        assert response.status_code == 200
