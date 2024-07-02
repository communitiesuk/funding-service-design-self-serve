from flask import Flask

from jinja2 import PackageLoader, ChoiceLoader
from flask_assets import Bundle
from jinja2 import PrefixLoader
from app.blueprints.self_serve.routes import self_serve_bp
from app.blueprints.dev.routes import dev_bp
from flask_assets import Environment
from os import getenv
import static_assets
from app.db.models import Fund, Round

def create_app() -> Flask:

    flask_app = Flask("__name__", static_url_path="/assets")
    flask_app.secret_key="dev"
    flask_app.register_blueprint(self_serve_bp)
    flask_app.register_blueprint(dev_bp)

    flask_app.config.from_mapping({
        "SQLALCHEMY_DATABASE_URI": getenv("DATABASE_URL", "postgresql://postgres:password@fsd-self-serve-db:5432/fund_builder")
    })

    flask_app.static_folder = "app/static/dist"

    from app.db import db, migrate

    # Bind SQLAlchemy ORM to Flask app
    db.init_app(flask_app)
    # Bind Flask-Migrate db utilities to Flask app
    migrate.init_app(
        flask_app,
        db,
        directory="app/db/migrations",
        render_as_batch=True,
        compare_type=True,
        compare_server_default=True,
    )

    # Bundle and compile assets
    assets = Environment()
    assets.init_app(flask_app)

    static_assets.init_assets(
        flask_app,
        auto_build=True,
        static_folder="app/static/dist",
    )

    flask_app.jinja_loader = ChoiceLoader(
        [
            PackageLoader("app"),
            PrefixLoader({"govuk_frontend_jinja": PackageLoader("govuk_frontend_jinja")}),
        ]
    )


    return flask_app

app = create_app()