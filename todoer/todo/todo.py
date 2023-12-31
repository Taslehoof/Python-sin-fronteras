from flask import(
    Blueprint, flash, g, redirect, render_template, request, url_for
        )
from werkzeug.exceptions import abort
from todo.auth import login_required
from todo.db import get_db

bp = Blueprint('todo', __name__)


@bp.route('/')
@login_required
def index():
    db, c = get_db()
    c.execute(
        'select t.id, t.description, u.username, t.completed, t.created_at from todo t JOIN user u on t.created_by = u.id order by created_at desc'
            )
    todos = c.fetchall()

    return render_template('todo/index.html', todos=todos)


@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        description = request.form['description']
        error = None

        if not description:
            error = 'Descripcion es requerida'

        if error is not None:
            flash(error)
        else:
            db, c = get_db()
            c.execute(
                'insert into todo(description, completed, created_by)'
                ' values (%s,%s,%s)',
                (description, False, g.user['id'])
            )
            db.commit()
            return redirect(url_for('todo.index'))
    return render_template('todo/create.html')


def get_todo(id):
    db, c = get_db()
    c.execute(
        'select t.idm t.description, t.completed, t.created_by, t.created_at, u.username '
        'from todo t join user u on t.created_by = u.id where t.id = %s',
        (id,)
    )
    todo = c.fetchone()
    if todo is None:
        abort(404, "El todo de id {0} no existe.".format(id))

    return todo


@bp.route('/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update(id):
    todo = get_todo(id)

    if request.method == 'post':
        description = request.form['description']
        completed = True if request.form.get('completed')== 'on' else False
        error = None

    if not description:
        error = "La descripcion es requerida."

    return render_template('todo/update.html', todo={
        "description": "Mi todo",
        "id": 2,
        "competed": 0
        })

@bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete():
    return ''
