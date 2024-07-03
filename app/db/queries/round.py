from app.db import db
from app.db.models.round import Round


def add_round(round: Round) -> Round:
    db.session.add(round)
    db.session.commit()
    return round
