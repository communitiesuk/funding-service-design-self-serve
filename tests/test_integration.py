import pytest
from flask_migrate import upgrade
from sqlalchemy import text

from app.app import create_app
from app.db.models import Form
from app.db.models import Fund
from app.db.queries.fund import get_all_funds
from app.question_reuse.generate_form import build_form_json
from tasks.test_data import insert_test_data

url_base = "postgresql://postgres:password@fsd-self-serve-db:5432/fund_builder"  # pragma: allowlist secret


@pytest.fixture(scope="session")
def app():
    app = create_app(config={"SQLALCHEMY_DATABASE_URI": f"{url_base}_unit_test"})
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


def test_build_form_json(_db, flask_test_client):
    _db.session.execute(text("TRUNCATE TABLE fund, round, section,form, page, component CASCADE;"))
    _db.session.commit()
    insert_test_data(_db)

    f: Fund = get_all_funds()[0]
    form: Form = f.rounds[0].sections[0].forms[0]

    result = build_form_json(form=form)
    assert result
    # TODO check results!
