import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db.session import get_db
from app.db.base import Base
from app.api.deps import get_current_applicant

# Use an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)

@pytest_asyncio.fixture
async def db_session():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with TestingSessionLocal() as session:
        yield session
        await session.rollback()

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture
async def client(db_session):
    async def override_get_db():
        try:
            yield db_session
        finally:
            pass # Session is handled by the fixture

    app.dependency_overrides[get_db] = override_get_db
    # Using AsyncClient for async support
    async with AsyncClient(app=app, base_url="http://test") as c:
        yield c
    app.dependency_overrides.clear()

# Mock user for authentication
class MockUser:
    def __init__(self, id=1, email="test@example.com"):
        self.id = id
        self.email = email

@pytest_asyncio.fixture
async def auth_client(client):
    async def override_get_current_applicant():
        return MockUser()

    app.dependency_overrides[get_current_applicant] = override_get_current_applicant
    yield client
    app.dependency_overrides.pop(get_current_applicant, None)
