""" Flask Application Factory Pattern
http://flask.pocoo.org/docs/0.11/patterns/appfactories/

Conventions to follow for magic to ensue:

VIEWS, MODELS, and COMMANDS ("bundles")
-----------------------------
All views/models should be contained in bundle folders.
Views should be in a file named `views.py` containing the flask.Blueprint instance.
Models should be in a file named `models.py` and should extend database.Model
Commands should be in a file named `commands.py` containing a click.Group instance.
Finally, each bundle folder must be registered in `config.py`

EXTENSIONS
-----------------------------
All extensions should be instantiated in `extensions.py`

CLI COMMANDS
-----------------------------
Decorate custom CLI commands in `commands.py` using @cli.command()

FLASK SHELL CONTEXT
-----------------------------
Database models and app extensions will automatically be added to
the shell context, presuming the above conventions have been followed.
"""
import sys
from flask import Flask

from .logger import logger
from .magic import (
    get_commands,
    get_extensions,
    get_bundle_blueprints,
    get_bundle_models,
    get_bundle_command_groups,
)


def create_app(config_object, **kwargs):
    """Application factory"""
    app = Flask(__name__, **kwargs)
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    register_shell_context(app)
    register_cli_commands(app)
    return app


def register_extensions(app):
    """Register and initialize extensions"""
    for extension in get_extensions():
        extension.init_app(app)


def register_blueprints(app):
    """Register bundle views"""
    # disable strict_slashes on all routes by default
    if not app.config.get('STRICT_SLASHES', False):
        app.url_map.strict_slashes = False
    # register blueprints
    for blueprint, url_prefix in get_bundle_blueprints():
        app.register_blueprint(blueprint, url_prefix=url_prefix)


def register_shell_context(app):
    """Register variables to automatically import when running `flask shell`"""
    def shell_context():
        # extensions
        ctx = dict(get_extensions())
        # DB models
        ctx.update(dict(get_bundle_models()))
        return ctx
    app.shell_context_processor(shell_context)


def register_cli_commands(app):
    """Register all the Click commands declared in commands.py and
    each bundle's commands.py"""
    commands = list(get_commands())
    commands += list(get_bundle_command_groups())
    for name, command in commands:
        if name in app.cli.commands:
            logger.error('Command name conflict: "%s" is taken.' % name)
            sys.exit(1)
        app.cli.add_command(command)
