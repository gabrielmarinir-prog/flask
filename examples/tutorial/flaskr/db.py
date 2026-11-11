import click
from flaskr.models import db


def init_db():
    """Limpa os dados existentes e recria as tabelas usando os Modelos."""
    db.drop_all()
    db.create_all()


@click.command("init-db")
def init_db_command():
    """Comando CLI para recriar as tabelas do banco de dados."""
    init_db()
    click.echo("Banco de dados inicializado com Flask-SQLAlchemy.")


def init_app(app):
    """Registra o comando CLI init-db na aplicação Flask."""
    app.cli.add_command(init_db_command)
