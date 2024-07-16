import pytest
from flask_migrate import upgrade

from app.app import create_app

url_base = "postgresql://postgres:password@fab-db:5432/fab"  # pragma: allowlist secret


@pytest.fixture(scope="session")
def app():
    app = create_app(config={"SQLALCHEMY_DATABASE_URI": url_base})
    yield app


@pytest.fixture(scope="function")
def flask_test_client():
    with create_app(
        config={"SQLALCHEMY_DATABASE_URI": f"{url_base}_unit_test"}  # pragma: allowlist secret
    ).app_context() as app_context:
        upgrade()
        with app_context.app.test_client() as test_client:
            yield test_client


@pytest.fixture(scope="session")
def _db(app, request):
    """
    Fixture to supply tests with direct access to the database
    """

    yield app.extensions["sqlalchemy"]
