import pytest
from unittest.mock import MagicMock
from app.services.google import oauth

@pytest.mark.asyncio
async def test_login_redirect(client, mocker):
    """
    Test that /login redirects to Google.
    """
    mock_authorize = mocker.patch.object(oauth.google, 'authorize_redirect')
    mock_authorize.return_value = "http://google.com/auth"

    response = await client.get("/api/v1/auth/login")
    
    assert mock_authorize.called

@pytest.mark.asyncio
async def test_callback_creates_user(client, mocker, mock_db_session):
    """
    Test that /callback receives a code, exchanges it for a token, gets user info,
    and upserts the user in the DB.
    """
    mock_token = {"access_token": "fake-token", "userinfo": {
        "email": "test@example.com",
        "name": "Test User",
        "picture": "http://img.com/pic.jpg",
        "sub": "12345"
    }}
    mocker.patch.object(oauth.google, 'authorize_access_token', return_value=mock_token)

    mock_result = MagicMock()
    mock_result.scalars.return_value.first.return_value = None
    mock_db_session.execute.return_value = mock_result

    response = await client.get("/api/v1/auth/callback?code=fakecode")

    assert response.status_code == 307
    assert "token=" in response.headers["location"]
    
    assert mock_db_session.add.called
    assert mock_db_session.commit.called
