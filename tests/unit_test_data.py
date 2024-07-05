from uuid import uuid4

from app.db.models import Component
from app.db.models import ComponentType
from app.db.models import Criteria
from app.db.models import Form
from app.db.models import Page
from app.db.models import Subcriteria
from app.db.models import Theme

form_1_id = uuid4()
page_1_id = uuid4()
section_1_id = uuid4()
theme_1_id = uuid4()
crit_1_id = uuid4()
sc_1_id = uuid4()
mock_c_1 = Component(
    component_id=uuid4(),
    type=ComponentType.TEXT_FIELD,
    title="Organisation name",
    hint_text="This must match your registered legal organisation name",
    page_id=page_1_id,
    page_index=1,
    theme_id=theme_1_id,
)
mock_c_2 = Component(
    component_id=uuid4(),
    type=ComponentType.EMAIL_ADDRESS_FIELD,
    title="What is your email address?",
    hint_text="Work not personal",
    page_id=page_1_id,
    page_index=2,
    theme_id=theme_1_id,
)
mock_p_1 = Page(
    page_id=page_1_id,
    name_in_apply={"en": "A test page"},
    display_path="test-display-path",
    components=[mock_c_1, mock_c_2],
    form_id=form_1_id,
)
mock_form_1 = Form(
    form_id=form_1_id,
    pages=[mock_p_1],
    section_id=section_1_id,
    name_in_apply={"en": "A test form"},
    runner_publish_name="a-test-form",
)
t1: Theme = Theme(
    theme_id=theme_1_id,
    subcriteria_id=sc_1_id,
    name="General Information",
    subcriteria_index=1,
    components=[mock_c_1, mock_c_2],
)
sc1: Subcriteria = Subcriteria(
    subcriteria_id=sc_1_id, criteria_index=1, criteria_id=crit_1_id, name="Organisation Information", themes=[t1]
)
cri1: Criteria = Criteria(criteria_id=crit_1_id, index=1, name="Unscored", weighting=0.0, subcriteria=[sc1])
