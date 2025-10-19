import pytest
import sys
from unittest.mock import patch, MagicMock

# Mock openai before importing app
with patch('openai.OpenAI') as mock_openai:
    mock_client = MagicMock()
    mock_openai.return_value = mock_client
    from app import app, get_client

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_review_code_success(client, mocker):
    mock_response = MagicMock()
    mock_response.choices[0].message.content = "Good code"
    mocker.patch('app.get_client').return_value.chat.completions.create.return_value = mock_response

    response = client.post('/review', data='def test(): pass')
    assert response.status_code == 200
    assert b'Good code' in response.data

def test_review_code_error(client, mocker):
    mocker.patch('app.get_client').return_value.chat.completions.create.side_effect = Exception("Some error")

    response = client.post('/review', data='def test(): pass')
    assert response.status_code == 200
    assert b'Error in AI review' in response.data

def test_review_code_openai_rate_limit(client, mocker):
    mocker.patch('app.get_client').return_value.chat.completions.create.side_effect = Exception("Rate limit exceeded")

    response = client.post('/review', data='def test(): pass')
    assert response.status_code == 200
    assert b'Error in AI review' in response.data