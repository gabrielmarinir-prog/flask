import os
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, current_app
)
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename
from flaskr.auth import login_required
from flaskr.models import db, Post

bp = Blueprint('blog', __name__)

def save_post_image(image_file):
    if image_file and image_file.filename != '':
        filename = secure_filename(image_file.filename)
        upload_folder = os.path.join(current_app.root_path, 'static', 'uploads')
        os.makedirs(upload_folder, exist_ok=True)
        image_file.save(os.path.join(upload_folder, filename))
        return filename
    return None

def get_post(id, check_author=True):
    post = Post.query.get(id)

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post.author_id != g.user.id:
        abort(403)

    return post


@bp.route('/')
def index():
    # Retorna todos os posts em ordem decrescente de criação
    posts = Post.query.order_by(Post.created.desc()).all()
    return render_template('blog/index.html', posts=posts)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        image_file = request.files.get('imagem_post')
        error = None

        if not title:
            error = 'Title is required.'

        if error is None:
            filename = save_post_image(image_file)
            
            post = Post(
                title=title,
                body=body,
                author_id=g.user.id,
                imagem_post=filename
            )
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('blog.index'))

        flash(error)

    return render_template('blog/create.html')


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        image_file = request.files.get('imagem_post')
        error = None

        if not title:
            error = 'Title is required.'

        if error is None:
            post.title = title
            post.body = body
            
            filename = save_post_image(image_file)
            if filename:
                post.imagem_post = filename

            db.session.commit()
            return redirect(url_for('blog.index'))

        flash(error)

    return render_template('blog/update.html', post=post)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    post = get_post(id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('blog.index'))