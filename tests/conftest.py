import pytest
import asyncio
from typing import AsyncGenerator, Generator
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.main import app
from app.db.base import Base
from app.api.deps import get_db
from app.core.config import settings

import pytest_asyncio

@pytest_asyncio.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as c:
        yield c

@pytest.fixture
def mock_db_session(mocker):
    """Mocks the database session dependency."""
    mock_session = mocker.Mock(spec=AsyncSession)
    app.dependency_overrides[get_db] = lambda: mock_session
    return mock_session
