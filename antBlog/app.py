# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
import logging
import sys

from flask import Flask, render_template

from antblog import commands, user
from antblog.user.models import User
from antblog.extensions import (
    bcrypt,
    cache,
    db,
    debug_toolbar,
    flask_static_digest,
    migrate,
    guard,
)


def create_app(config_object="antblog.settings"):
    """Create application factory, as explained here: http://flask.pocoo.org/docs/patterns/appfactories/.

    :param config_object: The configuration object to use.
    """
    app = Flask(__name__.split(".")[0])
    app.config.from_object(config_object)
    register_blueprints(app)
    print("//////////////////////////////////////////////////////////")
    with app.app_context():
        register_extensions(app)
        # db.create_all()
        db.session.add(
            User(
                username="Maude",
                password=guard.hash_password("andthorough"),
            )
        )
        db.session.commit()
    register_errorhandlers(app)
    register_shellcontext(app)
    register_commands(app)
    configure_logger(app)
    return app


def register_extensions(app):
    """Register Flask extensions."""
    bcrypt.init_app(app)
    cache.init_app(app)
    db.init_app(app)
    guard.init_app(app, user.models.User)
    debug_toolbar.init_app(app)
    migrate.init_app(app, db)
    flask_static_digest.init_app(app)

    return None


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(user.views.blueprint)
    return None


def register_errorhandlers(app):
    """Register error handlers."""

    def render_error(error):
        """Render error template."""
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, "code", 500)
        return render_template(f"{error_code}.html"), error_code

    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)(render_error)
    return None


def register_shellcontext(app):
    """Register shell context objects."""

    def shell_context():
        """Shell context objects."""
        return {"db": db, "User": user.models.User}

    app.shell_context_processor(shell_context)


def register_commands(app):
    """Register Click commands."""
    app.cli.add_command(commands.test)
    app.cli.add_command(commands.lint)


def configure_logger(app):
    """Configure loggers."""
    handler = logging.StreamHandler(sys.stdout)
    if not app.logger.handlers:
        app.logger.addHandler(handler)
