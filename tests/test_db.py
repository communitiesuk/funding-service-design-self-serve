from datetime import datetime
from random import randint
from uuid import uuid4

import pytest
from flask_migrate import upgrade
from sqlalchemy import text

from app.app import create_app
from app.db.models import Fund
from app.db.models import Round, Page
from app.db.queries.fund import add_fund
from app.db.queries.fund import get_all_funds
from app.db.queries.fund import get_fund_by_id
from app.db.queries.round import add_round
from app.db.queries.round import get_round_by_id

from app.db.queries.application import get_template_page_by_display_path

url_base = "postgresql://postgres:password@fsd-self-serve-db:5432/fund_builder"  # pragma: allowlist secret


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


def test_add_fund(flask_test_client, _db):
    f = Fund(
        name_json={"en": "hello"},
        title_json={"en": "longer hello"},
        description_json={"en": "reeeaaaaallly loooooooog helloooooooooo"},
        welsh_available=False,
        short_name=f"X{randint(0,99999)}",
    )
    result = add_fund(f)
    assert result
    assert result.fund_id


def test_add_round(flask_test_client, _db):
    fund = _db.session.execute(text("select * from fund limit 1;")).one()
    result = add_round(
        Round(
            fund_id=fund.fund_id,
            audit_info={"user": "dummy_user", "timestamp": datetime.now().isoformat(), "action": "create"},
            title_json={"en": "test title"},
            short_name=f"Z{randint(0,99999)}",
            opens=datetime.now(),
            deadline=datetime.now(),
            assessment_start=datetime.now(),
            reminder_date=datetime.now(),
            assessment_deadline=datetime.now(),
            prospectus_link="http://www.google.com",
            privacy_notice_link="http://www.google.com",
        )
    )
    assert result
    assert result.round_id


def test_get_all_funds(flask_test_client, _db):
    results = get_all_funds()
    assert results


def test_get_fund_by_id(flask_test_client, _db):
    any_fund = _db.session.execute(text("select * from fund limit 1;")).one()
    result: Fund = get_fund_by_id(any_fund.fund_id)
    assert result.name_json == any_fund.name_json


def test_get_fund_by_id_none(flask_test_client, _db):
    result: Fund = get_fund_by_id(str(uuid4()))
    assert result is None


def test_get_round_by_id_none(flask_test_client, _db):
    result: Round = get_round_by_id(str(uuid4()))
    assert result is None


def test_get_round_by_id(flask_test_client, _db):
    any_round = _db.session.execute(text("select * from round limit 1;")).one()
    result: Round = get_round_by_id(any_round.round_id)
    assert result.title_json == any_round.title_json


def test_get_template_page_by_display_path(flask_test_client, _db):
    _db.session.execute(
        text("TRUNCATE TABLE fund, round, section,form, page, component, theme, subcriteria, criteria CASCADE;")
    )
    _db.session.commit()
    
    template_page: Page = Page(
        page_id=uuid4(),
        form_id=None,
        display_path="testing_templates_path",
        is_template=True,
        name_in_apply={"en": "Template Path"},
        form_index=0,
    )
    non_template_page: Page = Page(
        page_id=uuid4(),
        form_id=None,
        display_path="testing_templates_path",
        is_template=False,
        name_in_apply={"en": "Not Template Path"},
        form_index=0,
    )
   
    _db.session.bulk_save_objects([template_page, non_template_page])
    _db.session.commit()
    result = get_template_page_by_display_path("testing_templates_path")
    assert result
    assert result.page_id == template_page.page_id