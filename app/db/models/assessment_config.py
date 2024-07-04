import uuid
from dataclasses import dataclass
from typing import List

from flask_sqlalchemy.model import DefaultMeta
from sqlalchemy import Column
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship
from sqlalchemy.types import Boolean

from app.db import db
from app.db.models import Component

BaseModel: DefaultMeta = db.Model


@dataclass
class Theme(BaseModel):
    theme_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    subcriteria_id = Column(
        UUID(as_uuid=True),
        ForeignKey("subcriteria.subcriteria_id"),
        nullable=True,
    )
    name = Column(String())
    template_name = Column("Template Name", String(), nullable=True)
    is_template = Column("is_template", Boolean, default=False, nullable=False)
    audit_info = Column("audit_info", JSON(none_as_null=True))
    components: Mapped[List["Component"]] = relationship("Component")
    subcriteria_index = Column(Integer())


@dataclass
class SubCriteria(BaseModel):
    subcriteria_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    criteria_id = Column(
        UUID(as_uuid=True),
        ForeignKey("criteria.criteria_id"),
        nullable=True,
    )
    name = Column(String())
    template_name = Column("Template Name", String(), nullable=True)
    is_template = Column("is_template", Boolean, default=False, nullable=False)
    audit_info = Column("audit_info", JSON(none_as_null=True))
    themes: Mapped[List["Theme"]] = relationship("Theme")
    criteria_index = Column(Integer())


@dataclass
class Criteria(BaseModel):
    criteria_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    round_id = Column(
        UUID(as_uuid=True),
        ForeignKey("round.round_id"),
        nullable=True,
    )
    name = Column(String())
    weighting = Column(Float(precision=2))
    template_name = Column("Template Name", String(), nullable=True)
    is_template = Column("is_template", Boolean, default=False, nullable=False)
    audit_info = Column("audit_info", JSON(none_as_null=True))
    index = Column(Integer())
