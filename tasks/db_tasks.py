

import sys

sys.path.insert(1, ".")
from invoke import task
from app.app import app


@task
def recreate_local_db(c):
    """Create a clean database for development.

    Unit testing makes a seperate db.

    """

    from sqlalchemy_utils.functions import create_database
    from sqlalchemy_utils.functions import database_exists, drop_database

    with app.app_context():
        db_uri = app.config.get("SQLALCHEMY_DATABASE_URI")
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
