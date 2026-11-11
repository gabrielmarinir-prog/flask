import functools
import os

from flask import (
    Blueprint, current_app, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from sqlalchemy.exc import IntegrityError

# Importa o db e o modelo User definidos em models.py
from flaskr.models import db, User

bp = Blueprint("auth", __name__, url_prefix="/auth")


def login_required(view):
    """View decorator que redireciona usuários não autenticados para o login."""
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))
        return view(**kwargs)

    return wrapped_view


@bp.before_app_request
def load_logged_in_user():
    """Carrega o usuário logado do banco de dados para g.user."""
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        # Sintaxe SQLAlchemy substituindo a consulta SQL pura
        g.user = db.session.get(User, user_id)


@bp.route("/register", methods=("GET", "POST"))
def register():
    """Registra um novo usuário com upload de foto de perfil (avatar)."""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        avatar_file = request.files.get("avatar")
        filename = None

        # Trata o upload da foto de perfil
        if avatar_file and avatar_file.filename != '':
            filename = secure_filename(avatar_file.filename)
            avatar_file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

        error = None

        if not username:
            error = "Username is required."
        elif not password:
            error = "Password is required."

        if error is None:
            try:
                # Cria a instância da classe User (Model)
                user = User(
                    username=username,
                    password=generate_password_hash(password),
                    avatar=filename or 'default_avatar.png'
                )
                db.session.add(user)
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template("auth/register.html")


@bp.route("/login", methods=("GET", "POST"))
def login():
    """Autentica o usuário utilizando a busca por SQLAlchemy."""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        error = None

        # Busca o usuário pelo username via SQLAlchemy
        user = User.query.filter_by(username=username).first()

        if user is None:
            error = "Incorrect username."
        elif not check_password_hash(user.password, password):
            error = "Incorrect password."

        if error is None:
            session.clear()
            session["user_id"] = user.id
            return redirect(url_for("index"))

        flash(error)

    return render_template("auth/login.html")


@bp.route("/logout")
def logout():
    """Limpa a sessão atual."""
    session.clear()
    return redirect(url_for("index"))