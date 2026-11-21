import os
from unittest.mock import Mock

import pytest

os.environ["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

from app import app
from config.cache import cache
from config.database import db


@pytest.fixture(autouse=True)
def clean_database():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    with app.app_context():
        assert db.engine.url.drivername == "sqlite"
        cache.redis_client = Mock()
        cache.redis_client.get.return_value = None
        db.create_all()
        yield
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client():
    return app.test_client()
