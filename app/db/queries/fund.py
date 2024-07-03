from app.db import db
from app.db.models.fund import Fund


def add_fund(fund: Fund) -> Fund:
    db.session.add(fund)
    db.session.commit()
    return fund
