import os
from datetime import date
from pathlib import Path

from flask import Flask

from .db import init_db
from .routes import bp


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", "local-development-key"),
        DATABASE=os.environ.get(
            "DATABASE", str(Path(app.instance_path) / "daymark.sqlite")
        ),
    )

    if test_config:
        app.config.update(test_config)

    Path(app.instance_path).mkdir(parents=True, exist_ok=True)

    @app.template_filter("date_label")
    def format_date(value):
        return date.fromisoformat(value).strftime("%b %-d")

    app.register_blueprint(bp)
    init_db(app)
    return app
