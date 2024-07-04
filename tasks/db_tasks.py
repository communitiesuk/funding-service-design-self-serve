import sys

sys.path.insert(1, ".")
from invoke import task  # noqa:E402

from app.app import app  # noqa:E402

from .test_data import insert_test_data  # noqa:E402


@task
def recreate_local_dbs(c):
    """Create a clean database for development.

    Unit testing makes a seperate db.

    """

    from sqlalchemy_utils.functions import create_database
    from sqlalchemy_utils.functions import database_exists
    from sqlalchemy_utils.functions import drop_database

    with app.app_context():
        for db_uri in [
            "postgresql://postgres:password@fsd-self-serve-db:5432/fund_builder",  # pragma: allowlist secret
            "postgresql://postgres:password@fsd-self-serve-db:5432/fund_builder_unit_test",  # pragma: allowlist secret
        ]:
            if database_exists(db_uri):
                print("Existing database found!\n")
                drop_database(db_uri)
                print("Existing database dropped!\n")
            else:
                print(
                    f"{db_uri} not found...",
                )
            create_database(db_uri)
            print(
                f"{db_uri} db created...",
            )


@task
def create_test_data(c):
    """Inserts some initial test data"""
    from sqlalchemy import text

    with app.app_context():
        db = app.extensions["sqlalchemy"]
        db.session.execute(text("TRUNCATE TABLE fund, round, section,form, page, component CASCADE;"))
        db.session.commit()
        insert_test_data(db=db)
