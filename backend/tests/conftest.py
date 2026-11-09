from datetime import datetime, timezone

import pytest
from fastapi.testclient import TestClient

from app.config import Settings
from app.main import create_app
from app.seed import seed

# Monday 10:00 UTC: inside calling hours for every seeded market.
FIXED_NOW = datetime(2026, 11, 9, 10, 0, tzinfo=timezone.utc)
API_KEY = "test-key"


@pytest.fixture
def app(tmp_path):
    settings = Settings(_env_file=None, database_url=f"sqlite:///{tmp_path / 'test.db'}", api_key=API_KEY, log_level="WARNING")
    application = create_app(settings)
    runtime = application.state.runtime
    runtime.container.clock = lambda: FIXED_NOW
    with runtime.session_factory() as db:
        seed(db)
    return application


@pytest.fixture
def client(app):
    with TestClient(app, headers={"X-API-Key": API_KEY}) as c:
        yield c
