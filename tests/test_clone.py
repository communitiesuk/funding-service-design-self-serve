from uuid import uuid4

from app.db.models import Component
from app.db.models import ComponentType
from app.db.models import Page
from app.db.queries.application import _initiate_cloned_component
from app.db.queries.application import clone_multiple_components
from app.db.queries.application import clone_single_component


def test_initiate_cloned_component(mocker):
    mocker.patch("app.db.queries.application.uuid4", return_value="123-456-789")
    clone: Component = Component(
        component_id="old-id",
        page_id="pre-clone",
        title="Template qustion 1?",
        type=ComponentType.TEXT_FIELD,
        page_index=1,
        theme_id="pre-clone",
        theme_index=2,
        options={"hideTitle": False, "classes": "test-class"},
        runner_component_name="template_question_name",
        conditions={"a": "b"},
    )
    result = _initiate_cloned_component(clone, "old-id", "page-123", "theme-234")

    assert result

    # Check new ID
    assert result.component_id == "123-456-789"

    # Check other bits are the same
    assert result.title == clone.title
    assert result.type == clone.type
    assert result.options == clone.options
    assert result.conditions == clone.conditions

    # check template settings
    assert result.is_template is False
    assert result.source_template_id == "old-id"

    assert result.page_id == "page-123"
    assert result.theme_id == "theme-234"


def test_clone_single_component(flask_test_client, _db):
    template_component: Component = Component(
        component_id=uuid4(),
        page_id=None,
        title="Template qustion 1?",
        type=ComponentType.YES_NO_FIELD,
        page_index=1,
        theme_id=None,
        theme_index=2,
        options={"hideTitle": False, "classes": "test-class"},
        runner_component_name="template_question_name",
    )

    _db.session.bulk_save_objects([template_component])
    _db.session.commit()

    result = clone_single_component(template_component.component_id)
    assert result

    # Check new ID
    assert result.component_id != template_component.component_id

    # Check other bits are the same
    assert result.title == template_component.title
    assert result.type == template_component.type
    assert result.options == template_component.options
    assert result.conditions is None

    # check template settings
    assert result.is_template is False
    assert result.source_template_id == template_component.component_id

    # Check new component exists in db
    from_db = _db.session.query(Component).where(Component.component_id == result.component_id).one_or_none()
    assert from_db


def test_clone_multiple_components(flask_test_client, _db):

    page: Page = Page(
        page_id=uuid4(),
        form_id=None,
        display_path="testing_clones",
        is_template=False,
        name_in_apply={"en": "Clone testing"},
        form_index=0,
    )

    template_component_1: Component = Component(
        component_id=uuid4(),
        page_id=None,
        title="Template qustion 1?",
        type=ComponentType.YES_NO_FIELD,
        page_index=1,
        theme_id=None,
        theme_index=2,
        options={"hideTitle": False, "classes": "test-class"},
        runner_component_name="template_question_name_1",
    )

    template_component_2: Component = Component(
        component_id=uuid4(),
        page_id=None,
        title="Template qustion 2?",
        type=ComponentType.YES_NO_FIELD,
        page_index=1,
        theme_id=None,
        theme_index=2,
        options={"hideTitle": False, "classes": "test-class"},
        runner_component_name="template_question_name_2",
    )

    template_component_3: Component = Component(
        component_id=uuid4(),
        page_id=None,
        title="Template qustion 3?",
        type=ComponentType.YES_NO_FIELD,
        page_index=1,
        theme_id=None,
        theme_index=2,
        options={"hideTitle": False, "classes": "test-class"},
        runner_component_name="template_question_name_3",
    )

    _db.session.bulk_save_objects([template_component_1, template_component_2, template_component_3, page])
    _db.session.commit()

    results = clone_multiple_components(
        component_ids=[
            template_component_1.component_id,
            template_component_2.component_id,
            template_component_3.component_id,
        ],
        new_page_id=page.page_id,
        new_theme_id=None,
    )
    assert results
    assert len(results) == 3

    # Check new component exists in db
    from_db = _db.session.query(Component).filter(Component.component_id.in_([c.component_id for c in results])).all()
    assert from_db
    assert len(from_db) == 3

    # Check they appear when the parent page now retrieved
    page_from_db = _db.session.query(Page).where(Page.page_id == page.page_id).one_or_none()
    assert page_from_db
    assert len(page_from_db.components) == 3
