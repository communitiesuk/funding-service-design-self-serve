import uuid
from dataclasses import dataclass
from enum import Enum
from typing import List

from flask_sqlalchemy.model import DefaultMeta
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship
from sqlalchemy.types import Boolean

from app.db import db

BaseModel: DefaultMeta = db.Model


class ComponentType(Enum):
    TEXT_FIELD = "TextField"
    FREE_TEXT_FIELD = "FreeTextField"
    EMAIL_ADDRESS_FIELD = "EmailAddressField"
    UK_ADDRESS_FIELD = "UkAddressField"
    HTML = "Html"
    YES_NO_FIELD = "YesNoField"


@dataclass
class Section(BaseModel):

    round_id = Column(
        "round_id",
        UUID(as_uuid=True),
        ForeignKey("round.round_id"),
        nullable=True,  # will be null where this is a template and not linked to a round
    )
    section_id = Column(
        "section_id",
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    name_in_apply = Column("name_in_apply_json", JSON(none_as_null=True), nullable=False, unique=False)
    template_name = Column("Template Name", String(), nullable=True)
    is_template = Column("is_template", Boolean, default=False, nullable=False)
    audit_info = Column("audit_info", JSON(none_as_null=True))
    forms: Mapped[List["Form"]] = relationship("Form")
    index = Column(Integer())


@dataclass
class Form(BaseModel):

    section_id = Column(
        "section_id",
        UUID(as_uuid=True),
        ForeignKey("section.section_id"),
        nullable=True,  # will be null where this is a template and not linked to a section
    )
    form_id = Column(
        "form_id",
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    name_in_apply = Column("name_in_apply_json", JSON(none_as_null=True), nullable=False, unique=False)
    template_name = Column("Template Name", String(), nullable=True)
    is_template = Column("is_template", Boolean, default=False, nullable=False)
    audit_info = Column("audit_info", JSON(none_as_null=True))
    section_index = Column("section_index", Integer())
    pages: Mapped[List["Page"]] = relationship("Page")


@dataclass
class Page(BaseModel):

    form_id = Column(
        "form_id",
        UUID(as_uuid=True),
        ForeignKey("form.form_id"),
        nullable=True,  # will be null where this is a template and not linked to a form
    )
    page_id = Column(
        "page_id",
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    name_in_apply = Column("name_in_apply_json", JSON(none_as_null=True), nullable=False, unique=False)
    template_name = Column("Template Name", String(), nullable=True)
    is_template = Column("is_template", Boolean, default=False, nullable=False)
    audit_info = Column("audit_info", JSON(none_as_null=True))
    form_index = Column(Integer())
    display_path = Column("display_path", String())
    components: Mapped[List["Component"]] = relationship("Component")


@dataclass
class Component(BaseModel):

    component_id = Column(
        "component_id",
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    page_id = Column(
        "page_id",
        UUID(as_uuid=True),
        ForeignKey("page.page_id"),
        nullable=True,  # will be null where this is a template and not linked to a page
    )
    theme_id = Column(
        UUID(as_uuid=True),
        ForeignKey("theme.theme_id"),
        nullable=True,  # will be null where this is a template and not linked to a theme
    )
    title = Column(String())
    hint_text = Column(String(), nullable=True)
    options = Column(JSON(none_as_null=False))
    type = Column(ENUM(ComponentType))
    template_name = Column("Template Name", String(), nullable=True)
    is_template = Column("is_template", Boolean, default=False, nullable=False)
    audit_info = Column("audit_info", JSON(none_as_null=True))
    page_index = Column(Integer())
    conditions = Column(JSON(none_as_null=True))
