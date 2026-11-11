import os
from flask import Flask
from flaskr.models import db  # Importa o db criado no models.py


def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)

    # Configurações atualizadas para SQLAlchemy e Uploads
    app.config.from_mapping(
        SECRET_KEY="dev",
        SQLALCHEMY_DATABASE_URI=f"sqlite:///{os.path.join(app.instance_path, 'flaskr.sqlite')}",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        UPLOAD_FOLDER=os.path.join(app.root_path, "static/uploads"),
    )

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.update(test_config)

    # Garante que a pasta instance existe
    os.makedirs(app.instance_path, exist_ok=True)

    # Inicializa o SQLAlchemy com o app e cria as tabelas
    db.init_app(app)

    with app.app_context():
        db.create_all()

    # Registra os blueprints (auth, blog e calculos)
    from . import auth, blog, calculos

    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)
    app.register_blueprint(calculos.bp)

    app.add_url_rule("/", endpoint="index")

    return app