from random import randint

import pytest
from flask import Flask
from flask_migrate import upgrade

from app.app import create_app
from app.db.models.fund import Fund
from app.db.queries.fund import add_fund

url_base = "postgresql://postgres:password@fsd-self-serve-db:5432/fund_builder"  # pragma: allowlist secret


@pytest.fixture(scope="session")
def app() -> Flask:
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


def test_add_fund(flask_test_client, _db):
    f = Fund(
        name_json={"en": "hello"},
        title_json={"en": "longer hello"},
        description_json={"en": "reeeaaaaallly loooooooog helloooooooooo"},
        welsh_available=False,
        short_name=f"H{randint(0,99999)}",
    )
    result = add_fund(f)
    assert result
    assert result.id
