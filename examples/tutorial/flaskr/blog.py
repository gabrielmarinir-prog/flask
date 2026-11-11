import os
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, current_app
)
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename

from flaskr.auth import login_required
from flaskr.models import db, Post

bp = Blueprint('blog', __name__)


def get_post(id, check_author=True):
    """Busca um post pelo ID e verifica se o usuário logado é o autor."""
    post = db.session.get(Post, id)

    if post is None:
        abort(404, f"Post id {id} não encontrado.")

    if check_author and post.author_id != g.user.id:
        abort(403)

    return post


@bp.route('/')
def index():
    """Lista todos os posts do mais recente ao mais antigo."""
    posts = Post.query.order_by(Post.created.desc()).all()
    return render_template('blog/index.html', posts=posts)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    """Cria um novo post com suporte a upload de imagem."""
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        image_file = request.files.get('imagem_post')
        filename = None

        if image_file and image_file.filename != '':
            filename = secure_filename(image_file.filename)
            image_file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

        if not title:
            flash('Título é obrigatório.')
        else:
            post = Post(title=title, body=body, author_id=g.user.id, imagem_post=filename)
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    """Edita um post existente e atualiza/substitui a imagem se enviada."""
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        image_file = request.files.get('imagem_post')

        if not title:
            flash('Título é obrigatório.')
        else:
            post.title = title
            post.body = body

            # Se uma nova imagem for enviada, atualiza o campo
            if image_file and image_file.filename != '':
                filename = secure_filename(image_file.filename)
                image_file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                post.imagem_post = filename

            db.session.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    """Exclui um post do banco de dados."""
    post = get_post(id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('blog.index'))