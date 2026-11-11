import os
from flask import Flask
from flaskr.models import db
from . import db as db_cli


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    db_path = os.path.join(app.instance_path, "flaskr.sqlite")

    app.config.from_mapping(
        SECRET_KEY="dev",
        SQLALCHEMY_DATABASE_URI=f"sqlite:///{db_path}",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Inicializa o SQLAlchemy e comandos CLI
    db.init_app(app)
    db_cli.init_app(app)

    with app.app_context():
        db.create_all()

    # Registro dos Blueprints da aplicação
    from . import auth, blog, calculos

    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)
    app.register_blueprint(calculos.bp)

    app.add_url_rule("/", endpoint="index")

    return app