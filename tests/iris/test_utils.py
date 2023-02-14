from unittest.mock import AsyncMock
from unittest.mock import patch

import pytest
from app.iris.models import InputIris
from app.iris.models import OutputIris
from app.iris.utils import get_iris_prediction

@pytest.mark.asyncio
@patch("app.iris.utils.settings")
@patch("app.iris.utils.store.bento_client.session")
async def test_successful_get_iris_prediction(mock_session, mock_settings):

    # Mock the post method to return the mock response object
    mock_response = AsyncMock()
    mock_response.status = 200
    mock_response.json.return_value = ["setosa"]
    mock_session.post.return_value.__aenter__.return_value = mock_response

    mock_settings.pickle_model_name = "sample_model"

    test_input = InputIris(
        **{
            "SepalLengthCm": 4.4,
            "SepalWidthCm": 3.2,
            "PetalLengthCm": 1.3,
            "PetalWidthCm": 0.2
        }
    )

    test = await get_iris_prediction(test_input)

    assert test == OutputIris(output="setosa", model_name="sample_model")


@pytest.mark.asyncio
@patch("app.iris.utils.settings")
@patch("app.iris.utils.store.bento_client.session")
async def test_failed_bento_get_iris_prediction(mock_session, mock_settings):
    # Mock the post method to return the mock response object
    mock_response = AsyncMock()
    mock_response.status = 500
    mock_response.json.return_value = []
    mock_session.post.return_value.__aenter__.return_value = mock_response

    mock_settings.pickle_model_name = "sample_model"

    test_input = InputIris(
        **{
            "SepalLengthCm": 4.4,
            "SepalWidthCm": 3.2,
            "PetalLengthCm": 1.3,
            "PetalWidthCm": 0.2
        }
    )

    test = await get_iris_prediction(test_input)

    assert test == OutputIris(
        output="Error in prediction endpoint",
        model_name="sample_model"
    )


@pytest.mark.asyncio
@patch("app.iris.utils.settings")
@patch("app.iris.utils.store.bento_client.session")
async def test_empty_bento_resp_get_iris_prediction(mock_session, mock_settings):
    # Mock the post method to return the mock response object
    mock_response = AsyncMock()
    mock_response.status = 200
    mock_response.json.return_value = []
    mock_session.post.return_value.__aenter__.return_value = mock_response

    mock_settings.pickle_model_name = "sample_model"

    test_input = InputIris(
        **{
            "SepalLengthCm": 4.4,
            "SepalWidthCm": 3.2,
            "PetalLengthCm": 1.3,
            "PetalWidthCm": 0.2
        }
    )

    test = await get_iris_prediction(test_input)

    assert test == OutputIris(
        output="Error in prediction endpoint",
        model_name="sample_model"
    )


@pytest.mark.asyncio
@patch("app.iris.utils.settings")
@patch("app.iris.utils.store.bento_client.session")
async def test_500_bento_get_iris_prediction(mock_session, mock_settings):
    # Mock the post method to return the mock response object
    mock_session.post.return_value.__aenter__.side_effect = Exception()

    mock_settings.pickle_model_name = "sample_model"

    test_input = InputIris(
        **{
            "SepalLengthCm": 4.4,
            "SepalWidthCm": 3.2,
            "PetalLengthCm": 1.3,
            "PetalWidthCm": 0.2
        }
    )

    test = await get_iris_prediction(test_input)

    assert test == OutputIris(
        output="Error in prediction endpoint",
        model_name="sample_model"
    )
