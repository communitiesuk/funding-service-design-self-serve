from app.db import db
from app.db.models import Component
from app.db.models import Form
from app.db.models import Page


def get_form_for_component(component: Component) -> Form:
    page_id = component.page_id
    page = db.session.query(Page).where(Page.page_id == page_id).one_or_none()
    form = db.session.query(Form).where(Form.form_id == page.form_id).one_or_none()
    return form
