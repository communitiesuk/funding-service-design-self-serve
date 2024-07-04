from app.db import db
from app.db.models.fund import Fund


def add_fund(fund: Fund) -> Fund:
    db.session.add(fund)
    db.session.commit()
    return fund


def get_all_funds() -> list:
    query = db.session.query(Fund).order_by(Fund.short_name)
    return query.all()
