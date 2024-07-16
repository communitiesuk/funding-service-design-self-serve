from uuid import uuid4

from app.db import db
from app.db.models import Component
from app.db.models import Form
from app.db.models import Lizt
from app.db.models import Page


def get_form_for_component(component: Component) -> Form:
    page_id = component.page_id
    page = db.session.query(Page).where(Page.page_id == page_id).one_or_none()
    form = db.session.query(Form).where(Form.form_id == page.form_id).one_or_none()
    return form


def get_template_page_by_display_path(display_path: str) -> Page:
    page = (
        db.session.query(Page)
        .where(Page.display_path == display_path)
        .where(Page.is_template == True)  # noqa:E712
        .one_or_none()
    )
    return page


def get_form_by_id(form_id: str) -> Form:
    form = db.session.query(Form).where(Form.form_id == form_id).one_or_none()
    return form


def get_component_by_id(component_id: str) -> Component:
    component = db.session.query(Component).where(Component.component_id == component_id).one_or_none()
    return component


def get_list_by_id(list_id: str) -> Lizt:
    lizt = db.session.query(Lizt).where(Lizt.list_id == list_id).one_or_none()
    return lizt


def _initiate_cloned_component(clone: Component, source_id: str, new_page_id=None, new_theme_id=None):
    clone.page_id = new_page_id
    clone.theme_id = new_theme_id
    clone.is_template = False
    clone.source_template_id = source_id
    clone.component_id = uuid4()
    return clone


def clone_single_component(component_id: str, new_page_id=None, new_theme_id=None) -> Component:
    component_to_clone: Component = (
        db.session.query(Component).where(Component.component_id == component_id).one_or_none()
    )
    db.session.expunge(component_to_clone)
    clone = _initiate_cloned_component(component_to_clone, component_to_clone.component_id, new_page_id, new_theme_id)

    db.session.add(clone)
    db.session.commit()

    return component_to_clone


def clone_multiple_components(component_ids: list[str], new_page_id=None, new_theme_id=None) -> list[Component]:
    components_to_clone: list[Component] = (
        db.session.query(Component).filter(Component.component_id.in_(component_ids)).all()
    )
    db.session.expunge_all()  # TODO is this ok or do we need to expunge each one separately?
    clones = [
        _initiate_cloned_component(
            clone=clone, source_id=clone.component_id, new_page_id=new_page_id, new_theme_id=new_theme_id
        )
        for clone in components_to_clone
    ]
    db.session.add_all(clones)
    db.session.commit()

    return clones
